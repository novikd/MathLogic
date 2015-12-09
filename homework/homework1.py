from expression.axioms import *

fin = open("hw1.proof", "r")
fout = open("hw1.out", "w")

line = fin.readline().rstrip()
print(line, file=fout)
list = line.split("|-")
assumptions = {}
if len(list) == 2:
    line = list[0].split(",")
    for i in range(len(line)):
        if line[i] != "":
            assumptions[parseExp(line[i])] = i + 1
else:
    line = list

expressions = {}
list = []
line_number = 1
while True:
    line = fin.readline().rstrip()
    if not line:
        break

    temp = parseExp(line)

    state = 0
    num = -1

    # Проверяем является ли выражение предположением
    if temp in assumptions:
        state = 1
        num = assumptions[temp]

    # Проверяем является ли выражение аксиомой
    if state == 0:
        for i in range(len(axiomsExp)):
            if is_axiom(temp, axiomsExp[i]):
                state = 2
                num = i + 1
                break

    # Проверка на Modus Ponens
    if state == 0:
        for i in range(len(list) - 1, -1, -1):
            tmp = Implication(list[i], temp)
            if tmp in expressions:
                state = 3
                num = expressions[list[i]], expressions[tmp]
                break

    print("(", line_number, ") ", line, " ", end="", file=fout)
    if state == 0:
        print("(Не доказано)", sep="", file=fout)
    elif state == 1:
        print("(Предположение ", num, ")", sep="", file=fout)
    elif state == 2:
        print("(Сх. акс. ", num, ")", sep="", file=fout)
    else:
        first, second = num
        print("(М.Р. ", first, ", ", second, ")", sep="", file=fout)

    if state != 0:
        expressions[temp] = line_number
        list.append(temp)
    line_number += 1


fin.close()
fout.close()