from expression.expression import *


class FormalParser:
    def __init__(self):
        self.string = ""
        self.index = 0

    def parseExpr(self, string):
        self.index = 0
        self.string = string
        return self.__parseImplication()

    def parse(self):
        if self.index >= len(self.string):
            return None
        return self.__parseImplication()

    def __readVarName(self):
        j = self.index
        while j < len(self.string) and (
            self.string[j].isdigit() or (self.string[j].isalpha() and self.string[j].islower())):
            j += 1
        result = self.string[self.index:j]
        self.index = j
        return result

    def __readPredicateName(self):
        j = self.index
        while j < len(self.string) and (
            self.string[j].isdigit() or (self.string[j].isalpha() and self.string[j].isupper())):
            j += 1
        result = self.string[self.index:j]
        self.index = j
        return result

    def __parseImplication(self):
        result = self.__parseDisjuction()
        if self.index < len(self.string) and self.string[self.index] == '-':
            self.index += 2
            tmp = self.__parseImplication()
            return Implication(result, tmp)
        else:
            return result

    def __parseDisjuction(self):
        result = self.__parseConjuction()
        while self.index < len(self.string) and self.string[self.index] == '|':
            self.index += 1
            tmp = self.__parseConjuction()
            result = Disjuction(result, tmp)
        return result

    def __parseConjuction(self):
        result = self.__parseUnary()
        while self.index < len(self.string) and self.string[self.index] == '&':
            self.index += 1
            tmp = self.__parseUnary()
            result = Conjuction(result, tmp)
        return result

    def __parseUnary(self):
        if self.string[self.index] == '!':
            self.index += 1
            tmp = self.__parseUnary()
            return Not(tmp)
        elif self.string[self.index] == '@' or self.string[self.index] == '?':
            symbol = self.string[self.index]
            self.index += 1
            word = self.__readVarName()
            tmp = self.__parseUnary()
            if symbol == '@':
                return Any(Var(word), tmp)
            else:
                return Exists(Var(word), tmp)

        result = self.__parsePredicate()
        if not (result is None):
            return result

        if self.index < len(self.string) and self.string[self.index] == '(':
            self.index += 1
            result = self.__parseImplication()
            self.index += 1
            return result

    def __parsePredicate(self):
        word = self.__readPredicateName()
        if word != "":
            args = self.__parseArguments()
            return Predicate(word, args)
        else:
            save = self.index
            result = self.__parseTerm()
            if self.index >= len(self.string) or self.string[self.index] != '=':
                self.index = save
                return None
            self.index += 1
            return Equals(result, self.__parseTerm())

    def __parseArguments(self):
        result = list()
        if self.index >= len(self.string) or self.string[self.index] != '(':
            return result
        self.index += 1
        result.append(self.__parseTerm())
        while self.index < len(self.string) and self.string[self.index] != ')':
            self.index += 1
            result.append(self.__parseTerm())
        self.index += 1
        return result

    def __parseTerm(self):
        result = self.__parseSum()
        while self.index < len(self.string) and self.string[self.index] == '+':
            self.index += 1
            tmp = self.__parseSum()
            result = Sum(result, tmp)

        return result

    def __parseSum(self):
        result = self.__parseMul()
        while self.index < len(self.string) and self.string[self.index] == '*':
            self.index += 1
            tmp = self.__parseMul()
            result = Mul(result, tmp)

        return result

    def __parseMul(self):
        result = None
        if self.index < len(self.string) and self.string[self.index] == '(':
            self.index += 1
            result = self.__parseTerm()
            self.index += 1
            return self.__parseNext(result)
        word = self.__readVarName()
        if self.index < len(self.string) and self.string[self.index] == '(':
            values = self.__parseArguments()
            result = Predicate(word, values)
        else:
            result = Var(word)
        return self.__parseNext(result)

    def __parseNext(self, val):
        while self.index < len(self.string) and self.string[self.index] == '\'':
            self.index += 1
            val = Next(val)
        return val