from expression.parser import *

axioms = [
    "A -> (B -> A)",
    "(A -> B) -> (A -> B -> C) -> (A -> C)",
    "A -> B -> A & B",
    "A & B -> A",
    "A & B -> B",
    "A -> A | B",
    "A -> B | A",
    "(A -> B) -> (C -> B) -> (A | C -> B)",
    "(A -> B) -> (A -> !B) -> !A",
    "!!A -> A"
]

axiomsExp = [parseExp(string) for string in axioms]


def is_any_axiom(expr):
    for i in range(len(axiomsExp)):
        if is_axiom(expr, axiomsExp[i]):
            return True

    return False


def subtract(expr, values):
    if type(expr) is Var:
        return values[expr.val]
    elif type(expr) is Not:
        expr.val = subtract(expr.val, values)
    else:
        expr.left = subtract(expr.left, values)
        expr.right = subtract(expr.right, values)

    expr.rehash()
    return expr


def createExpr(string, values):
    return subtract(parseExp(string), values)


def addProof(address, proof, values):
    fin = open(address, "r")
    while True:
        line = fin.readline().rstrip()
        if not line:
            break

        proof.append(createExpr(line, values))
    fin.close()


class Proof(object):
    def __init__(self, expr, values):
        self.expression = expr
        self.assumptions = values
        self.expressions = []

    def deduction(self):
        new_expressions = []
        for i in range(len(self.expressions)):
            if self.expressions[i] == self.assumptions[0]:
                sub = {"A": self.expressions[i]}
                addProof("Proofs/|-A->A.proof", new_expressions, sub)
                continue

            if self.expressions[i] in self.assumptions or is_any_axiom(self.expressions[i]):
                sub = {"A": self.expressions[i], "B": self.assumptions[0]}
                new_expressions.append(self.expressions[i])
                new_expressions.append(createExpr("A->B->A", sub))
                new_expressions.append(createExpr("B->A", sub))
                continue

            for j in range(i - 1, -1, -1):
                tmp = Implication(self.expressions[j], self.expressions[i])
                if tmp in self.expressions:
                    sub = {"A": self.assumptions[0], "B": self.expressions[j], "C": self.expressions[i], "D": tmp}
                    new_expressions.append(createExpr("(A->B)->(A->D)->(A->C)", sub))
                    new_expressions.append(createExpr("(A->D)->(A->C)", sub))
                    new_expressions.append(createExpr("A->C", sub))
                    break
        self.expression = Implication(self.assumptions[0], self.expression)
        self.assumptions.pop(0)
        self.expressions = new_expressions

    def merge(self, other):
        sub = {"A": self.assumptions[0], "B": other.assumptions[0], "C": self.expression}

        self.deduction()
        other.deduction()

        sub["D"] = self.expression
        sub["E"] = other.expression

        self.expressions.extend(other.expressions)
        self.expressions.append(createExpr("D->E->(A|B->C)", sub))
        self.expressions.append(createExpr("E->(A|B->C)", sub))
        self.expressions.append(createExpr("(A|B->C)", sub))

        addProof("Proofs/A|!A.proof", self.expressions, sub)
        self.expressions.append(sub["C"])
        self.expression = sub["C"]

    def print(self, file_name):
        for i in range(len(self.assumptions)):
            if i == len(self.assumptions) - 1:
                print(self.assumptions[i], end=" ", file=file_name)
            else:
                print(self.assumptions[i], end=", ", file=file_name)
        print("|-", self.expression, end="\n", file=file_name)
        for i in range(len(self.expressions)):
            print(self.expressions[i], end="\n", file=file_name)


def createProof(expr, proof):
    if type(expr) is Var:
        if expr in proof.assumptions:
            proof.expressions.append(expr)
            return True
        else:
            proof.expressions.append(Not(expr))
            return False
    elif type(expr) is Not:
        A = createProof(expr.val, proof)
        sub = {"A": expr.val}
        if A:
            addProof("Proofs/A|-!!A.proof", proof.expressions, sub)
        return not A
    else:
        A = createProof(expr.left, proof)
        B = createProof(expr.right, proof)
        address = "Proofs/"
        if type(expr) is Implication:
            address += "Implication/"
        elif type(expr) is Conjuction:
            address += "And/"
        else:
            address += "Or/"

        if A:
            if B:
                address += "A_B.proof"
            else:
                address += "A_nB.proof"
        else:
            if B:
                address += "nA_B.proof"
            else:
                address += "nA_nB.proof"

        sub = {"A": expr.left, "B": expr.right}
        addProof(address, proof.expressions, sub)

        if proof.expressions[-1] == expr:
            return True
        else:
            return False
