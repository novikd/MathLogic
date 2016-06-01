proofPrefix = [ "0=0->0=0->0=0",
                "a=b->a=c->b=c",
                "(a=b->a=c->b=c)->(0=0->0=0->0=0)->(a=b->a=c->b=c)",
                "(0=0->0=0->0=0)->(a=b->a=c->b=c)",
                "(0=0->0=0->0=0)->@c(a=b->a=c->b=c)",
                "(0=0->0=0->0=0)->@b@c(a=b->a=c->b=c)",
                "(0=0->0=0->0=0)->@a@b@c(a=b->a=c->b=c)",
                "@c(a=b->a=c->b=c)",
                "@c(a=b->a=c->b=c)->(a=b->a=a->b=a)",
                "a=b->a=a->b=a",
                "@a@b@c(a=b->a=c->b=c)",
                "@a@b@c(a=b->a=c->b=c)->@b@c(a+0=b->a+0=c->b=c)",
                "(0=0->0=0->0=0)->@a@b@c(a=b->a=c->b=c)",
                "@b@c(a+0=b->a+0=c->b=c)->@c(a+0=a->a+0=c->a=c)",
                "@b@c(a+0=b->a+0=c->b=c)",
                "@c(a+0=a->a+0=c->a=c)",
                "@c(a+0=a->a+0=c->a=c)->(a+0=a->a+0=a->a=a)",
                "a+0=a->a+0=a->a=a",
                "a+0=a",
                "a+0=a->a=a",
                "a=a",
                "a=a->a=b->a=a",
                "a=b->a=a",
                "(a=b->a=a)->(a=b->a=a->b=a)->(a=b->b=a)",
                "(a=b->a=a->b=a)->(a=b->b=a)",
                "a=b->b=a",
                "(a=b->b=a)->(0=0->0=0->0=0)->(a=b->b=a)",
                "(0=0->0=0->0=0)->(a=b->b=a)",
                "(0=0->0=0->0=0)->@b(a=b->b=a)",
                "(0=0->0=0->0=0)->@a@b(a=b->b=a)",
                "@a@b(a=b->b=a)",
                "@a@b(a=b->b=a)->@b(x=b->b=x)",
                "@b(x=b->b=x)",
                "@b(x=b->b=x)->(x=y->y=x)",
                "x=y->y=x",
                "(x=y->y=x)->(0=0->0=0->0=0)->(x=y->y=x)",
                "(0=0->0=0->0=0)->(x=y->y=x)",
                "(0=0->0=0->0=0)->@y(x=y->y=x)",
                "(0=0->0=0->0=0)->@x@y(x=y->y=x)",
                "@x@y(x=y->y=x)"
                ]

proofStep = ["a+b'=(a+b)'",
             "a+b'=(a+b)'->(A->B->A)->a+b'=(a+b)'",
             "(A->B->A)->a+b'=(a+b)'",
             "(A->B->A)->@b(a+b'=(a+b)')",
             "A->B->A",
             "@b(a+b'=(a+b)')",
             "@b(a+b'=(a+b)')->(a+o'=(a+o)')",
             "a+o'=(a+o)'",
             "@x@y(x=y->y=x)->@y((a+o')=y->y=(a+o'))",
             "@y((a+o')=y->y=(a+o'))",
             "@y((a+o')=y->y=(a+o'))->(a+o')=(a+o)'->(a+o)'=(a+o')",
             "(a+o')=(a+o)'->(a+o)'=(a+o')",
             "(a+o)'=(a+o')",
             "a=b->a=c->b=c",
             "(a=b->a=c->b=c)->(A->B->A)->(a=b->a=c->b=c)",
             "(A->B->A)->(a=b->a=c->b=c)",
             "(A->B->A)->@c(a=b->a=c->b=c)",
             "(A->B->A)->@b@c(a=b->a=c->b=c)",
             "(A->B->A)->@a@b@c(a=b->a=c->b=c)",
             "(A->B->A)",
             "@a@b@c(a=b->a=c->b=c)",
             "@a@b@c(a=b->a=c->b=c)->@b@c((a+o)'=b->(a+o)'=c->b=c)",
             "@b@c((a+o)'=b->(a+o)'=c->b=c)",
             "@b@c((a+o)'=b->(a+o)'=c->b=c)->@c((a+o)'=(a+o')->(a+o)'=c->(a+o')=c)",
             "@c((a+o)'=(a+o')->(a+o)'=c->(a+o')=c)",
             "@c((a+o)'=(a+o')->(a+o)'=c->(a+o')=c)->((a+o)'=(a+o')->(a+o)'=d'->(a+o')=d')",
             "((a+o)'=(a+o')->(a+o)'=d'->(a+o')=d')",
             "(a+o)'=d'->(a+o')=d'",
             "a+o=d",
             "a=b->a'=b'",
             "(a=b->a'=b')->(A->B->A)->(a=b->a'=b')",
             "(A->B->A)->(a=b->a'=b')",
             "(A->B->A)->@b(a=b->a'=b')",
             "(A->B->A)->@a@b(a=b->a'=b')",
             "@a@b((a=b)->(a'=b'))",
             "@a@b((a=b)->(a'=b'))->@b((a+o=b)->(a+o)'=b')",
             "@b((a+o=b)->(a+o)'=b')",
             "@b((a+o=b)->(a+o)'=b')->((a+o=d)->(a+o)'=d')",
             "(a+o=d)->(a+o)'=d'",
             "(a+o)'=d'",
             "a+o'=d'"
             ]

proofEnd = ["a+o=d",
            "(a+o=d)->(A->B->A)->(a+o=d)",
            "(A->B->A)->(a+o=d)",
            "(A->B->A)->@a(a+o=d)",
            "(A->B->A)",
            "@a(a+o=d)",
            "@a(a+o=d)->(q+o=f)",
            "q+o=f"
            ]

a, b = map(int, input().rstrip().split())
result = a + b
lhs = "0" + ("'" * a)
rhs = "0" + ("'" * b)

print("|-", lhs, "+", rhs, "=", "0" + ("'" * result), sep="")

for line in proofPrefix:
    print(line)

currentO = "0"
currentA = "a"
for i in range(b):
    for line in proofStep:
        print(line.replace('o', currentO).replace('d', currentA))
    currentO += "'"
    currentA += "'"

currentQ = "0" + ("'" * a)
currentRes = "0" + ("'" * (a + b))
for line in proofEnd:
    print(line.replace('d', currentA).replace('o', currentO).replace('q', currentQ).replace('f', currentRes))
