from expression.utils import *

fin = open("hw3.in", "r")
fout = open("hw3.out", "w")

expr = parseExp(fin.readline().rstrip())
fin.close()
check = is_tautology(expr)
if len(check) > 0:
    print("Выражение ложно при ", end="", file=fout)
    first = True
    for e in check:
        if not first:
            print(", ", sep="", end="", file=fout)
        else:
            first = False
        if check[e]:
            print(e, "=И", sep="", end="", file=fout)
        else:
            print(e, "=Л", sep="", end="", file=fout)
else:
    tmp = {}
    get_variables(expr, tmp)
    variables = {}
    for e in tmp:
        variables[tmp[e]] = e
    proofs = []

    for mask in range(0, 2 ** len(variables)):
        assumptions = []
        for j in range(len(variables)):
            if mask & (2 ** j) == 0:
                assumptions.append(Var(variables[j]))
            else:
                assumptions.append(Not(Var(variables[j])))
        proof = Proof(expr, assumptions)
        createProof(expr, proof)
        proofs.append(proof)

    for i in range(len(variables)):
        new_proofs = []
        for j in range(0, len(proofs), 2):
            proofs[j].merge(proofs[j + 1])
            new_proofs.append(proofs[j])
        proofs = new_proofs

    proofs[0].print(fout)

fout.close()
