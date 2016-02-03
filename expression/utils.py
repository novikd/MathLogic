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
    expressions = []

    def __init__(self, expr, values):
        self.expression = expr
        self.assumptions = values

    def deduction(self):
        new_expressions = []
        for i in range(len(self.expressions)):
            if self.expressions[i] in self.assumptions or is_any_axiom(self.expressions[i]):
                sub = {"A" : self.expressions[i], "B" : self.assumptions[-1]}
                new_expressions.append(self.expressions[i])
                new_expressions.append(createExpr("A->B->A", sub))
                new_expressions.append(createExpr("B-A", sub))
                continue

            if self.expressions[i] == self.assumptions[-1]:
                sub = {"A" : self.expressions[i]}
                addProof("Proofs/|-A->A.proof", new_expressions, sub)
                continue

            for j in range(i - 1, -1, -1):
                tmp = Implication(self.expressions[j], self.expressions[i])
                if tmp in self.expressions:
                    sub = {"A" : self.assumptions[-1], "B": self.expressions[j], "C" : self.expressions[i], "D" : tmp}
                    new_expressions.append(createExpr("(A->B)->(A->D)->(A->C)", sub))
                    new_expressions.append(createExpr("(A->D)->(A->C)", sub))
                    new_expressions.append(createExpr("A->C", sub))
                    break
        self.expression = Implication(self.assumptions[-1], self.expression)
        self.assumptions.pop()


    def merge(self, other):
        # TODO: finish realization of this method
        raise NotImplementedError


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
        sub = {"A" : expr.val}
        if A:
            addProof("Proofs/A|-!!A.proof", proof.expressions, sub)
        else:
            proof.expressions.append(subtract("!A", sub))
        return not A
    else:
        A = createProof(expr.left, proof)
        B = createProof(expr.right, proof)
        # TODO: finish realization of this method