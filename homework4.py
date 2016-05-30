from expression.utils import *
fin = open("hw4.in", "r")
fout = open("hw4.out", "w")

parser = FormalParser()
line, main_expression = fin.readline().rstrip().split("|-")
assumptions = set()
parser.string = line
free_variables = set()
while parser.index < len(parser.string):
    tmp = parser.parse()
    assumptions.add(tmp)
    get_free_variables(tmp, set(), free_variables)
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
    error_string = "Неизвестная ошибка"
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
                if expression.right.var not in get_free_variables(expression.left, set(), set()):
                    if expression.right.var not in free_variables:
                        check = 3, tmp
                    else:
                        error_string = "Применение правил с кваторами, используещее свободные переменные из предположений."
                else:
                    error_string = "Ошибка применения правил вывода с кванторами. Переменная входит свободно."

    if check[0] == -1:
        if type(expression) is Implication and type(expression.left) is Exists:
            tmp = Implication(expression.left.val, expression.right)
            if tmp in expressions:
                if expression.right.var not in get_free_variables(expression.right, set(), set()):
                    if expression.left.var not in free_variables:
                        check = 4, tmp
                    else:
                        error_string = "Применение правил с кваторами, используещее свободные переменные из предположений."
                else:
                    error_string = "Ошибка применения правил вывода с кванторами. Переменная входит свободно."


    if check[0] == -1:
        print("Вывод некорректен, начиная с формулы №", line_number,":", error_string, end="\n", file=fout)
        break
    else:
        expressions.add(expression)
        expression_list.append(expression)
        prior.append(check)

if check[0] != -1:
    print("Вывод корректен")
    for i in range(len(expression_list)):
        if prior[i][0] == 0:
            None
        elif prior[i][0] == 1:
            None
        elif prior[i][0] == 2:
            None
        elif prior[i][0] == 3:
            None
        elif prior[i][0] == 4:
            None

fin.close()
fout.close()
