from expression.utils import *


def solve():
    fin = open("hw4.in", "r")
    fout = open("hw4.out", "w")

    parser = FormalParser()
    line, main_expression = fin.readline().rstrip().split("|-")
    assumptions = set()
    parser.string = line
    free_variables = set()
    last_assumption = None
    while parser.index < len(parser.string):
        tmp = parser.parse()
        last_assumption = tmp
        assumptions.add(tmp)
        get_free_variables(tmp, dict(), free_variables)
        if parser.index < len(parser.string) and parser.string[parser.index] == ',':
            parser.index += 1
    parser.index += 2
    main_expression = parser.parseExpr(main_expression)
    expressions = set()
    expression_list = list()
    prior = list()
    line_number = 0
    check = False

    while True:
        line_number += 1
        error_string = "[Недоказаное утверждение]"
        line = fin.readline().rstrip()
        if not line:
            break
        expression = parser.parseExpr(line)
        check = -1, None

        if is_any_axiom(expression) or is_any_formal_axiom(expression):
            check = 0, None

        if check[0] == -1 and expression in assumptions:
            check = 1, None

        if check[0] == -1:
            for j in range(len(expression_list)):
                if Implication(expression_list[len(expression_list) - j - 1], expression) in expressions:
                    check = 2, expression_list[len(expression_list) - j - 1]
                    break

        if check[0] == -1:
            if type(expression) is Implication and type(expression.right) is Any:
                tmp = Implication(expression.left, expression.right.val)
                if tmp in expressions:
                    if expression.right.var not in get_free_variables(expression.left, dict(), set()):
                        if expression.right.var not in free_variables:
                            check = 3, tmp
                        else:
                            error_string = "[Применение правил с кватором всеобщности, используещее свободную переменную " \
                                           + expression.right.var.__str__() + " из предположений.]"
                    else:
                        error_string = "[Ошибка применения правил вывода с квантором всеобщности. Переменная " \
                                       + expression.right.var.__str__() + " входит свободно.]"

        if check[0] == -1:
            if type(expression) is Implication and type(expression.left) is Exists:
                tmp = Implication(expression.left.val, expression.right)
                if tmp in expressions:
                    if expression.left.var not in get_free_variables(expression.right, dict(), set()):
                        if expression.left.var not in free_variables:
                            check = 4, tmp
                        else:
                            error_string = "[Применение правил с кватором существования, используещее свободную переменную " \
                                           + expression.left.var.__str__() + " из предположений.]"
                    else:
                        error_string = "[Ошибка применения правил вывода с квантором существования. Переменная " \
                                       + expression.right.var.__str__() + "входит свободно.]"

        if check[0] == -1:
            print("Вывод некорректен, начиная с формулы №", line_number, ":", error_string, "\n", line, end="\n", file=fout)
            break
        else:
            expressions.add(expression)
            expression_list.append(expression)
            prior.append(check)

    if check[0] != -1:
        print("Вывод корректен")
        semicolomn = 0
        for e in assumptions:
            if e != last_assumption:
                print(e, sep="", end="", file=fout)
                if semicolomn < len(assumptions) - 1:
                    print(",", sep="", end="", file=fout)
                semicolomn += 1

        if len(assumptions) > 0:
            print("|-", Implication(last_assumption, main_expression), sep="", end="\n", file=fout)
            fany = open("Proofs/any_rule.proof", "r")
            any_proof = fany.readlines()
            fany.close()
            fexists = open("Proofs/exists_rule.proof", "r")
            exists_proof = fexists.readlines()
            fexists.close()
            for i in range(len(expression_list)):
                if prior[i][0] == 0:
                    # axiom
                    print(Implication(expression_list[i], Implication(last_assumption, expression_list[i])), file=fout)
                    print(expression_list[i], file=fout)
                    print(Implication(last_assumption, expression_list[i]), file=fout)
                elif prior[i][0] == 1:
                    # assumption
                    if expression_list[i] != last_assumption:
                        print(Implication(expression_list[i], Implication(last_assumption, expression_list[i])), file=fout)
                        print(expression_list[i], file=fout)
                        print(Implication(last_assumption, expression_list[i]), file=fout)
                    else:
                        tmp1 = Implication(last_assumption, Implication(last_assumption, last_assumption))
                        print(tmp1, file=fout)

                        tmp2 = Implication(last_assumption, Implication(Implication(last_assumption, last_assumption), last_assumption))
                        tmp3 = Implication(last_assumption, last_assumption)
                        print(Implication(tmp1, Implication(tmp2, tmp3)), file=fout)
                        print(Implication(tmp2, tmp3), file=fout)
                        print(tmp2, file=fout)
                        print(tmp3, file=fout)
                elif prior[i][0] == 2:
                    # Modus Ponens
                    tmp = Implication(last_assumption, Implication(prior[i][1], expression_list[i]))
                    tmp1 = Implication(last_assumption, prior[i][1])
                    tmp2 = Implication(last_assumption, expression_list[i])
                    print(Implication(tmp1, Implication(tmp, tmp2)), file=fout)
                    print(Implication(tmp, tmp2), file=fout)
                    print(tmp2, file=fout)
                elif prior[i][0] == 3:
                    # Any
                    mapping = {"A" : last_assumption, "B" : expression_list[i].left, "C" : expression_list[i].right.val}
                    for str in any_proof:
                        tempExpr = createExpr(parser, str.rstrip(), mapping)
                        print(tempExpr, file=fout)
                elif prior[i][0] == 4:
                    # Exists
                    mapping = {"A" : last_assumption, "B" : expression_list[i].left.val, "C" : expression_list[i].right}
                    for str in exists_proof:
                        print(createExpr(parser, str, mapping), file=fout)
        else:
            print("|-", main_expression, sep="", file=fout)
            for expr in expression_list:
                print(expr, file=fout)

    fin.close()
    fout.close()

solve()