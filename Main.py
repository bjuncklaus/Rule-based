import re

rootVariables = {}
variablesValues = {}
learnedVariables = {}
rules = {}
symbols = ["!", "&", "|"]

parser = re.compile('[a-zA-Z_]+')

def teachNew(var, string):
    if (var in rootVariables):
        print("The variable has already been defined.")
        return None
    else:
        rootVariables[var] = string
        variablesValues[var] = False

def teachExistent(var, bool):
    if (var not in variablesValues):
        print("The variable", var, "needs to be defined first. Use TEACH <ARG> <VAR> = <STRING>.")
        return None
    else:
        if (bool == "true"):
            value = True
        if (bool == "false"):
            value = False
        variablesValues[var] = value

def teachRule(rule, var):
    if (var not in rootVariables):
        print("The variable", var, "needs to be defined first. Use TEACH <ARG> <VAR> = <STRING>.")

    if(isValid(rule)):
        rules[rule] = var

def learn():
    print()


def isValid(string):
    variablesInRule = parser.findall(string)
    for var in variablesInRule:
        if (var not in rootVariables):
            print("The variable", var, "needs to be defined first. Use TEACH <ARG> <VAR> = <STRING>.")
            return False
    return True

def list():
    print("Root Variables:")
    for v in rootVariables:
        print("\t", v, "=", rootVariables[v])
    print()

    print("Learned Variables:")
    for v in learnedVariables:
        print("\t", v, "=", learnedVariables[v])
    print()

    print("Facts:")
    for v in variablesValues:
        if (variablesValues[v] == True):
            print("\t", v)
    print()

    print("Rules:")
    for v in rules:
        print("\t", v, "->", rules[v])




"""
Tests
"""
def testTeachNew():
    def test1(function, param1, param2):
        print("Testing", function.__name__, "with", str(param1), "and", str(param2))
        function(param1, param2)
        assert len(rootVariables) == 1
        assert len(variablesValues) == 1
        assert variablesValues[param1] == False
        print("All tests passed!")

    test1(teachNew, "S", "a")
    test1(teachNew, "S", "a")

    def test2(function, param1, param2):
        print("Testing", function.__name__, "with", str(param1), "and", str(param2))
        function(param1, param2)
        assert len(rootVariables) == 2
        assert len(variablesValues) == 2
        assert variablesValues[param1] == False
        print("All tests passed!")

    test2(teachNew, "B", "b")

testTeachNew()

def testTeachExistent():
    def test1(function, param1, param2):
        print("Testing", function.__name__, "with", str(param1), "and", str(param2))
        function(param1, param2)
        assert len(variablesValues) == 2
        assert variablesValues["S"] == False
        assert variablesValues["B"] == False
        print("All tests passed!")

    test1(teachExistent, "S", "false")

    def test2(function, param1, param2):
        print("Testing", function.__name__, "with", str(param1), "and", str(param2))
        function(param1, param2)
        assert len(variablesValues) == 2
        assert variablesValues["S"] == True
        assert variablesValues["B"] == False

    test2(teachExistent, "S", "true")

testTeachExistent()

def testTeachRule():
    def test1(function, param1, param2):
        print("Testing", function.__name__, "with", str(param1), "and", str(param2))
        function(param1, param2)
        assert len(rules) == 0
        print("All tests passed!")

    test1(teachRule, "(BANANA&ABACAXI)|!MORANGO", "B")

    def test2(function, param1, param2):
        print("Testing", function.__name__, "with", str(param1), "and", str(param2))
        function(param1, param2)
        assert len(rules) == 1
        assert rules[param1] == param2
        print("All tests passed!")

    test2(teachRule, "!S", "B")

testTeachRule()

def testIsValid():
    def test1(function, param1):
        print("Testing", function.__name__, "with", str(param1))
        assert function(param1) == False
        print("All tests passed!")

    test1(isValid, "BICICLET_A")

    def test2(function, param1):
        print("Testing", function.__name__, "with", str(param1))
        assert function(param1) == True
        print("All tests passed!")

    test2(isValid, "B|!S")

testIsValid()

list()