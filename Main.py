"""
Author: Bruno Juncklaus Martins
Computing ID: bjm3j
"""
import re

rootVariables = []
rootValues = {}
learnedFacts = {}
variablesValues = {}
variablesValuesFake = {}
learnedVariables = {}
learnedVariablesFake = {}
reasoning = []
rules = []
symbols = ["!", "&", "|"]

parser = re.compile('[a-zA-Z_]+')
parser2 = re.compile('[!&|a-zA-Z->]+')

def teachNew(var, string):
    if (var in [j for i in rootVariables for j in i]):
        return None
    else:
        rootVariables.append({var : string})
        variablesValues[var] = False
        variablesValuesFake[var] = False

def teachExistent(var, bool):
    if (var not in variablesValues):
        return None
    else:
        if (bool == "true"):
            value = True
        if (bool == "false"):
            value = False
        variablesValues[var] = value
        variablesValuesFake[var] = value

def teachRule(rule, var):
    if (var not in [j for i in rootVariables for j in i]):
        return None

    if(isValid(rule)):
        rules.append({rule : var})

def learn(query):
    for dict in rules:
        for rule in dict:
            individualRules = parser.findall(rule)
            newRule = rule

            rulesUsedToLearn = []
            for r in individualRules:
                if (query == False):
                    newRule = newRule.replace(r, str(variablesValues[r]))
                else:
                    newRule = newRule.replace(r, str(variablesValuesFake[r]))
                    rulesUsedToLearn.append(rootValues[r])

            learnedFacts[dict[rule]] = rulesUsedToLearn
            evaluate = newRule.replace("!", " not ").replace("|", " or ").replace("&", " and ")
            boolValue = eval(evaluate)

            if (query == False):
                global learnedVariablesFake
                if (boolValue == True & (dict[rule] not in learnedVariables)):
                    learnedVariables[dict[rule]] = rule
                    learnedVariablesFake = learnedVariables
                    teachExistent(dict[rule], "true")
                    learn(False)
            else:
                if (boolValue == True & (dict[rule] not in learnedVariablesFake)):
                    learnedVariablesFake[dict[rule]] = rule
                    variablesValuesFake[dict[rule]] = True
                    learn(True)

def query(q):
    for root in rootVariables:
        for dict in root:
            rootValues[dict] = root[dict]

    if (isValid(q)):
        variablesInQuery = parser.findall(q)
        if (len(variablesInQuery) > 1):
            factsTemp = {}
            ret = True
            for vq in variablesInQuery:
                if (variablesValuesFake[vq] == False):
                    ret = False
                else:
                    factsTemp[vq] = vq

                learn(True)
                for learned in learnedVariablesFake:
                    factsTemp[learned] = learnedVariablesFake[learned]

                for vq in variablesInQuery:
                    q = q.replace(vq, str(variablesValuesFake[vq]))

                newRule = q.replace("!", " not ").replace("|", " or ").replace("&", " and ")

                for vq in variablesInQuery:
                    if (vq in learnedFacts):
                        reasoning.append({"K" : vq})
                        reasoning.append({"B" : learnedFacts[vq]})
                    reasoning.append({"C" : rootValues[vq]})
                reasoning.append({"V" : eval(newRule)})

                return eval(newRule)
        else:
            if (variablesValuesFake[variablesInQuery[0]] == False):
                learn(True)
                for vq in variablesInQuery:
                    q = q.replace(vq, str(variablesValuesFake[vq]))

                newRule = q.replace("!", " not ").replace("|", " or ").replace("&", " and ")

                for vq in variablesInQuery:
                    if (vq in learnedFacts):
                        for l in learnedVariablesFake:
                            if (l != variablesInQuery[0] and l in learnedFacts):
                                reasoning.append({"K" : learnedFacts[l]})
                                reasoning.append({"B" : learnedFacts[l]})

                        if (vq not in learnedVariablesFake):
                            reasoning.append({"K" : vq})
                        reasoning.append({"B" : learnedFacts[vq]})
                    else:
                        reasoning.append({"K" : vq})

                reasoning.append({"C" : rootValues[variablesInQuery[0]]})
                reasoning.append({"V" : eval(newRule)})
                return eval(newRule)
            else:
                for vq in variablesInQuery:
                    q = q.replace(vq, str(variablesValuesFake[vq]))

                newRule = q.replace("!", " not ").replace("|", " or ").replace("&", " and ")

                reasoning.append({"K" : variablesInQuery[0]})
                reasoning.append({"C" : rootValues[variablesInQuery[0]]})
                reasoning.append({"V" : eval(newRule)})

                return eval(newRule)

    return (q in learnedVariablesFake)

def why(q):
    print(query(q))

    known = []
    because = []
    conclusion = []

    for dict in reasoning:
        for item in dict:
            if (item == "K"):
                if (isinstance(dict[item], list)):
                    for v in dict[item]:
                        if (v not in known):
                            known.append(v)
                else:
                    if (rootValues[dict[item]] not in known):
                        known.append(rootValues[dict[item]])
            if (item == "B"):
                if (isinstance(dict[item], list)):
                    for v in dict[item]:
                        if (v not in because):
                            because.append(v)
                else:
                    if (rootValues[dict[item]] not in because):
                        because.append(rootValues[dict[item]])
            if (item == "C"):
                conclusion.append(dict[item])
            if (item == "V"):
                if (dict[item] == False):
                    conclusion[0] = "THUS I CANNOT PROVE " + conclusion[0]
                else:
                    conclusion[0] = "I THUS KNOW THAT " + conclusion[0]

    print("I KNOW THAT", known, "BECAUSE", known, "I KNOW THAT", because, conclusion)

def isValid(string):
    variablesInRule = parser.findall(string)
    for var in variablesInRule:
        if (var not in [j for i in rootVariables for j in i]):
            return False
    return True

def listt():
    print("Root Variables:")
    for v in rootVariables:
        for r in v:
            print("\t", r, "=", v[r])
    print()

    print("Learned Variables:")
    for v in learnedVariables:
        for dict in rootVariables:
            for dictValue in dict:
                if (dictValue == v):
                    print("\t", v, "=", dict[dictValue])
    print()

    print("Facts:")
    for v in variablesValues:
        if (variablesValues[v] == True):
            print("\t", v)
    print()

    print("Rules:")
    for v in rules:
        for r in v:
            print("\t", r, "->", v[r])


def main():
    while (True):
        command = input("")
        individualCommand = parser2.findall(command)

        if ("Teach" in individualCommand):
            if ("-R" in individualCommand):
                teachNew(individualCommand[2], individualCommand[3])
            elif ("->" in individualCommand):
                teachRule(individualCommand[1], individualCommand[3])
            else:
                teachExistent(individualCommand[1], individualCommand[2])

        if ("List" in individualCommand):
            listt()

        if ("Learn" in individualCommand):
            learn(False)

        if ("Query" in individualCommand):
            print(query(individualCommand[1]))

        if ("Why" in individualCommand):
            why(individualCommand[1])

main()