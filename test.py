# from expression.utils import *
#
# p = FormalParser()
# a = p.parseExpr("A(x)->A(x)")

for n in range(1, 200):
    curr = 0
    digits = [0 for i in range(10)]

    def check():
        for i in range(10):
            if digits[i] == 0:
                return True
        return False

    while check():
        curr += n
        tmp = curr
        while tmp > 0:
            digits[int(tmp % 10)] = 1
            tmp /= 10
    print(n, " ", curr, " ", curr % n, end="\n")
