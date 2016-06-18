from expression.parser import *
from expression.formal_parser import *

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

formal_axioms = [
    "a=b->a'=b'",
    "a=b->a=c->b=c",
    "a'=b'->a=b",
    "!(a'=0)",
    "a+b'=(a+b)'",
    "a+0=a",
    "a*0=0",
    "a*b'=a*b+a"
]

axiomsExp = [parseExp(string) for string in axioms]
expression_parser = FormalParser()
formalAxioms = [expression_parser.parseExpr(string) for string in formal_axioms]


def is_any_axiom(expr):
    for i in range(len(axiomsExp)):
        if is_axiom(expr, axiomsExp[i]):
            return True

    return False


def subtract(expr, values):
    if type(expr) is Var:
        return expr
    elif type(expr) is Predicate:
        if expr.name in values:
            return values[expr.name]
        for i in range(len(expr.val)):
            expr[i] = subtract(expr.val[i], values)
    elif isinstance(expr, Unary):
        expr.val = subtract(expr.val, values)
    else:
        expr.left = subtract(expr.left, values)
        expr.right = subtract(expr.right, values)

    if (type(expr) is Any or type(expr) is Exists) and expr.var.val == "x":
        expr.var = values["x"].val

    expr.rehash()
    return expr


def createExpr(parser : FormalParser, string, values):
    return subtract(parser.parseExpr(string), values)


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
                addProof("Proofs/A_Implication_A.proof", new_expressions, sub)
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

        addProof("Proofs/Aor!A.proof", self.expressions, sub)
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
            addProof("Proofs/From_A_To_!!A.proof", proof.expressions, sub)
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


def free_subtract(template, exp, var, locked: dict, dictionary):
    if type(template) is Var:
        if template != var:
            return template == exp
        if template.val in locked:
            return template == exp
        else:
            if template in dictionary:
                return dictionary[template] == exp
            else:
                tmp = set()
                get_free_variables(exp, dict(), tmp)
                if len(tmp.intersection(locked)) != 0:
                    return False
                dictionary[template] = exp
                return True
    elif type(template) is type(exp):
        if type(template) is Any or type(template) is Exists:
            if template.var.val not in locked:
                locked[template.var.val] = 1
            else:
                locked[template.var.val] += 1
            result = free_subtract(template.val, exp.val, var, locked, dictionary)
            locked[template.var.val] -= 1
            if locked[template.var.val] == 0:
                locked.pop(template.var.val, None)
            return result
        elif type(template) is Predicate:
            if len(template.val) != len(exp.val):
                return False
            for i in range(len(template.val)):
                if not free_subtract(template.val[i], exp.val[i], var, locked, dictionary):
                    return False
            return True
        elif isinstance(template, Unary):
            return free_subtract(template.val, exp.val, var, locked, dictionary)
        else:
            if not free_subtract(template.left, exp.left, var, locked, dictionary):
                return False
            return free_subtract(template.right, exp.right, var, locked, dictionary)
    else:
        return False


def is_axiom_any(expr):
    if type(expr) is not Implication or type(expr.left) is not Any:
        return False
    return free_subtract(expr.left.val, expr.right, expr.left.var, dict(), dict())


def is_axiom_exists(expr):
    if type(expr) is not Implication or type(expr.right) is not Exists:
        return False
    return free_subtract(expr.right.val, expr.left, expr.right.var, dict(), dict())


def is_any_formal_axiom(expr):
    for axiom in formalAxioms:
        if new_match(axiom, expr, set(), dict()):
            return True
    if is_axiom_any(expr) or is_axiom_exists(expr):
        return True
    return False
