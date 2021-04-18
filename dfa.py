import sys
import json
import numpy as np
import time
stateCtr = -1
eps = '$'

def transition(s, a, tfunc):
    ret = []

    for tr in range(0, len(tfunc)):
        if(tfunc[tr][0] == s and tfunc[tr][1] == a and tfunc[tr][2] not in ret):
            ret.append(tfunc[tr][2])

    ret.sort()
    return ret[:]

def epsilon(R, transitions):
    ret = R[:]
    prev = []

    while(ret != prev):
        prev = ret[:]

        for transit in range(0, len(transitions)):
            if(transitions[transit][0] in ret and transitions[transit][1] == '$' and transitions[transit][2] not in ret):
                ret.append(transitions[transit][2])

    ret.sort()
    return ret[:]

def powerSet(stateSet, final):
    ret = []
    fin = []

    for i in range(0, pow(2, len(stateSet))):
        temp = []
        flag = False

        for j in range(0, len(stateSet)):
            if(i & (1 << j)):
                temp.append(stateSet[j])
                if(stateSet[j] in final):
                    flag = True

        ret.append(temp[:])
        if(flag):
            fin.append(temp[:])

    return [ret[:], fin[:]]

def parse(inp):

    [states, final_states] = powerSet(inp['states'][:], inp['final_states'][:])
    dfa = {
            "states": states,
            "letters": inp['letters'][:],
            "transition_function": [],
            "start_states": [epsilon(inp['start_states'][:], inp['transition_function'][:])],
            "final_states": final_states
    }

    for state in range(0, len(states)):
        for alpha in range(0, len(dfa['letters'])):
            to = []

            for r in range(0, len(states[state])):
                to = list(set(to).union(set(epsilon(transition(states[state][r], dfa['letters'][alpha], inp['transition_function']), inp['transition_function']))))

            to.sort()
            dfa['transition_function'].append([states[state], dfa['letters'][alpha], to])

    return dfa

def main():
    with open(sys.argv[1], "r") as file:
        inp = json.load(file)
    
    with open(sys.argv[2], "w") as file:
        json.dump(parse(inp), file, indent = 2)

if __name__ == "__main__":
    main()
