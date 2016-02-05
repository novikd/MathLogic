mod = (10 ** 9) + 9


class Expression(object):
    hash = 0

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


class Unary(Expression):
    def __init__(self, value):
        self.val = value


class Var(Unary):
    def __init__(self, value):
        self.hash = value.__hash__() % mod
        super().__init__(value)

    def __str__(self):
        return self.val

    def rehash(self):
        self.hash = self.val.__hash__()

    def eval(self, dictionary):
        return dictionary[self.val]


class Not(Unary):
    name = "!"

    def __init__(self, value):
        super().__init__(value)
        self.rehash()

    def __str__(self):
        return "(! " + self.val.__str__() + " )"

    def rehash(self):
        self.hash = (3 * self.val.__hash__() ** 2 + 7 * self.name.__hash__()) % mod

    def eval(self, dictionary):
        return not self.val.eval(dictionary)


class Binary(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.rehash()

    def __str__(self):
        return "( " + self.left.__str__() + self.name + self.right.__str__() + " )"

    def rehash(self):
        self.hash = (3 * self.name.__hash__() + 11 * self.left.__hash__()**3 + 23 * self.right.__hash__()**4) % mod

    def calc(self, left, right):
        raise NotImplementedError

    def eval(self, dictionary):
        return self.calc(self.left.eval(dictionary), self.right.eval(dictionary))


class Implication(Binary):
    name = " -> "

    def __init__(self, left, right):
        super().__init__(left, right)

    def calc(self, left, right):
        return (not left) or right


class Conjuction(Binary):
    name = " & "

    def __init__(self, left, right):
        super().__init__(left, right)

    def calc(self, left, right):
        return left and right


class Disjuction(Binary):
    name = " | "

    def __init__(self, left, right):
        super().__init__(left, right)

    def calc(self, left, right):
        return left or right


# Старый метод, больше не используется (Можно не читать)
def match(first, second) -> (bool, dict):
    if type(second) is Var:
        return True, {second.val: first}
    elif type(first) is type(second):
        if type(first) is Not:
            return match(first.val, second.val)
        else:
            res1, dict1 = match(first.left, second.left)
            res2, dict2 = match(first.right, second.right)

            if not res1 or not res2:
                return False, {}

            if type(dict1) is dict and type(dict2) is dict:
                for key in dict1:
                    if key in dict2 and dict1[key] != dict2[key]:
                        return False, {}

                for key in dict1:
                    if key not in dict2:
                        dict2[key] = dict1[key]
                return True, dict2
    else:
        return False, {}


def new_match(exp, axiom, dictionary):
    # Словарь передается по ссылке, поэтому нет смысла его копировать
    if type(axiom) is Var:
        # Присвоение переменной из аксиомы значения
        # Если эта переменная уже была проинициализированна, то возвращается False
        if axiom in dictionary:
            if dictionary[axiom] != exp:
                return False
            else:
                return True
        else:
            dictionary[axiom] = exp
            return True
    elif type(exp) is type(axiom):
        if type(axiom) is Not:
            return new_match(exp.val, axiom.val, dictionary)
        else:
            sub = new_match(exp.left, axiom.left, dictionary)
            # В sub хранится значение удалось ли удачно сделать подстановку в левом поддереве дерева разбора выражения
            if sub:
                sub = new_match(exp.right, axiom.right, dictionary)

            return sub
    else:
        # Тип выражений не совпал
        return False


# Функция проверяет является выражение exp аксиомой checking_axiom
def is_axiom(exp, checking_axiom):
    return new_match(exp, checking_axiom, {})


def get_variables(exp, dictionary: dict):
    if type(exp) is Var:
        if exp.val not in dictionary:
            dictionary[exp.val] = len(dictionary)
    elif type(exp) is Not:
        get_variables(exp.val, dictionary)
    else:
        get_variables(exp.left, dictionary)
        get_variables(exp.right, dictionary)


# Функция проверяет является ли выражение тавтологией
def is_tautology(exp):
    temp = dict()
    get_variables(exp, temp)
    dictionary = dict()
    for e in temp:
        dictionary[temp[e]] = e

    for bits in range(0, 2 ** len(dictionary)):
        temp = dict()
        for j in range(0, len(dictionary)):
            if bits & (2 ** j) == 0:
                temp[dictionary[j]] = False
            else:
                temp[dictionary[j]] = True

        if not exp.eval(temp):
            return temp

    return dict()
