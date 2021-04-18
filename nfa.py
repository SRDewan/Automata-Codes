import sys
import json
import numpy as np
stateCtr = -1
eps = '$'

def union(nfas):
    global stateCtr, eps
    nfa1 = nfas[0]
    nfa2 = nfas[1]
    stateCtr += 1
    newstate = "Q{}".format(stateCtr)

    result = {
            "states": nfa1['states'] + nfa2['states'],
            "letters": nfa1['letters'] + list(set(nfa2['letters']) - set(nfa1['letters'])),
            "transition_function": nfa1['transition_function'] + nfa2['transition_function'],
            "start_states": [newstate],
            "final_states": nfa1['final_states'] + nfa2['final_states'],
    }

    result['states'].append(newstate)
    result['transition_function'].append([newstate, eps, nfa1['start_states'][0]])
    result['transition_function'].append([newstate, eps, nfa2['start_states'][0]])

    return result

def concat(nfas):
    global stateCtr, eps
    nfa1 = nfas[0]
    nfa2 = nfas[1]

    result = {
            "states": nfa1['states'] + nfa2['states'],
            "letters": nfa1['letters'] + list(set(nfa2['letters']) - set(nfa1['letters'])),
            "transition_function": nfa1['transition_function'] + nfa2['transition_function'],
            "start_states": nfa1['start_states'],
            "final_states": nfa2['final_states'],
    }

    for fin in range(0, len(nfa1['final_states'])):
        end = nfa1['final_states'][fin]
        result['transition_function'].append([end, eps, nfa2['start_states'][0]])

    return result

def closure(nfa):
    global stateCtr, eps
    start = nfa['start_states'][0]
    stateCtr += 1
    newstate = "Q{}".format(stateCtr)

    nfa['states'].append(newstate)
    nfa['final_states'].append(newstate)

    for fin in range(0, len(nfa['final_states'])):
        end = nfa['final_states'][fin]
        nfa['transition_function'].append([end, eps, start])

    nfa['start_states'][0] = newstate
    return nfa

def basicNFA(alpha):
    global stateCtr, eps
    states = ["Q{}".format(stateCtr + 1), "Q{}".format(stateCtr + 2)]
    stateCtr += 2
    nfa = {
            "states": states,
            "letters": [alpha],
            "transition_function": [
                    [states[0], alpha, states[1]],
                ],
            "start_states": [states[0]],
            "final_states": [states[1]],
    }

    return nfa

def NFA(rex, operation):
    for i in range(0, len(rex)):
        if(isinstance(rex[i], str)):
            rex[i] = basicNFA(rex[i])

    if(operation == 2):
        rex = closure(rex[0])

    elif(operation == 1):
        rex = concat(rex)

    else:
        rex = union(rex)

    return rex

def postfix(strg, precedence):
    stack = []
    exp = ""

    for i in range(0, len(strg)):
        if(strg[i] == '('):
            stack.append(strg[i])

        elif(strg[i] == ')'):
            top = stack[len(stack) - 1]

            while(top != '('):
                exp += top
                stack.pop()
                top = stack[len(stack) - 1]

            stack.pop()

        elif(strg[i] in precedence.keys()):
            if(not len(stack)):
                stack.append(strg[i])
                continue

            top = stack[len(stack) - 1]

            while(top in precedence.keys() and precedence[top] >= precedence[strg[i]]):
                exp += top
                stack.pop()

                if(len(stack)):
                    top = stack[len(stack) - 1]

                else:
                    break

            stack.append(strg[i])

        else:
            exp += strg[i]

    for i in range(len(stack) - 1, -1, -1):
        exp += stack[i]

    return exp

def addDot(inp):
    ind = 0
    ctr = 0
    ret = ""

    while(ind in range(0, len(inp))):
        if(inp[ind] == ')'):
            return [ret, inp[ind:]]

        if(inp[ind] not in ['+', '*']):
            ctr += 1
            if(ctr == 2):
                ctr = 1
                ret += '.'

            if(inp[ind] == '('):
                temp = addDot(inp[ind + 1:])
                ret += '(' + temp[0]
                inp = temp[1]
                ind = 0

        elif(inp[ind] == '+'):
            ctr = 0

        ret += inp[ind]
        ind += 1

    return ret

def parse(inp, precedence):

    operation = 1  #2 => union, 1 => concat, 0 => *
    rex = []
    stack = []

    for symbol in range(0, len(inp)):
        if(inp[symbol] == '*'):
            rex[-1] = NFA(rex[-1:], precedence[inp[symbol]])

        elif(inp[symbol] in ['.', '+']):
            rex[-2] = NFA(rex[-2:], precedence[inp[symbol]])
            rex.pop()

        else:
            rex.append(inp[symbol])

    return rex[0]

def main():
    with open(sys.argv[1], "r") as file:
        inp = json.load(file)
    
    with open(sys.argv[2], "w") as file:
        precedence = {'+': 0, '.': 1, '*': 2}
        inp = postfix(addDot(inp['regex']), precedence)
        json.dump(parse(inp, precedence), file, indent = 2)

if __name__ == "__main__":
    main()
