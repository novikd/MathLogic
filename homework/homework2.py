from expression.axioms import *

fin = open("hw2.proof", "r")
fout = open("hw2.out", "w")

line = fin.readline().rstrip()
# print(line, file=fout)
list = line.split("|-")
assumptions = set()
last = Expression
line = list[0].split(",")
for i in range(len(line)):
    if line[i] != "":
        last = parseExp(line[i])
        assumptions.add(last)
        if i < len(line) - 2:
            print(line[i], ",", sep="", end=" ", file=fout)
        elif i == len(line) - 2:
            print(line[i], end=" ", file=fout)
        # assumptions[parseExp(line[i])] = i + 1
print("|-", line[-1], "->", list[1], file=fout)

expressions = {}
list = []
line_number = 0
while True:
    line = fin.readline().rstrip()
    if not line:
        break

    temp = parseExp(line)

    state = 0
    num = -1

    if last == temp:
        state = 1
        tmp1 = Implication(temp, Implication(temp, temp))
        print(tmp1, file=fout)

        tmp2 = Implication(temp, Implication(Implication(temp, temp), temp))
        tmp3 = Implication(temp, temp)
        print(Implication(tmp1, Implication(tmp2, tmp3)), file=fout)

        print(Implication(tmp2, tmp3), file=fout)

        print(tmp2, file=fout)
        print(tmp3, file=fout)

    if state == 0:
        if temp in assumptions:
            # print("Assumption", file=fout)
            state = 1
            print(Implication(temp, Implication(last, temp)), file=fout)
            print(temp, file=fout)
            print(Implication(last, temp), file=fout)

    if state == 0:
        for i in range(len(axiomsExp)):
            if is_axiom(temp, axiomsExp[i]):
                state = 1
                # print("Axiom", file=fout)
                print(Implication(temp, Implication(last, temp)), file=fout)
                print(temp, file=fout)
                print(Implication(last, temp), file=fout)
                break

    # TODO: rewrite creating an answer for Modus Ponens case
    if state == 0:
        for i in range(len(list) - 1, -1, -1):
            tmp = Implication(list[i], temp)
            if tmp in expressions:
                state = 2
                num = expressions[list[i]], expressions[tmp]
                break

    if state == 2:
        # print("Modus Ponens", file=fout)
        first, second = num
        print("(", last, "->", list[first] , end="", file=fout)
        print(") -> ( ", end="", file=fout)
        print(last, "-> (", list[second], ")", end = "", file=fout)
        print(") -> (", last, "->", line, ")", file = fout)
        print("( (", last, ") -> (", list[second], ") ) -> ", end="", file=fout)
        print("(", last , "->", line, ")", file = fout)
        print("(", last , "->", line, ")", file = fout)

    expressions[temp] = line_number
    list.append(temp)
    line_number += 1


fin.close()
fout.close()