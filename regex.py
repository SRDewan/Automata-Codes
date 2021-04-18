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

    return ret[:]

def stateRem(gnfa):
    remove = gnfa['states'][0]
    transmat = {}
    newtransit = []
    outgoing = []
    incoming = []
    loop = -1

    for t in range(0, len(gnfa['transition_function'])):
        trans = gnfa['transition_function'][t]
        concat = ''.join(trans[0]) + ''.join(trans[2])

        if(trans[0] == remove and trans[2] == remove):
            loop = t

        elif(trans[0] == remove): 
            outgoing.append(t)

        elif(trans[2] == remove): 
            incoming.append(t)

        else:
            newtransit.append(trans)
            transmat[concat] = len(newtransit) - 1

    for i in range(0, len(incoming)):
        for j in range(0, len(outgoing)):
            inn = gnfa['transition_function'][incoming[i]]
            out = gnfa['transition_function'][outgoing[j]]
            concat = ''.join(inn[0]) + ''.join(out[2])

            exp = ''
            if(inn[1] != '$'):
                exp = inn[1]

            if(loop != -1):
                exp += '(' + gnfa['transition_function'][loop][1] + ')*'

            if(out[1] != '$'):
                exp += out[1]

            if(concat not in transmat):
                newtransit.append([inn[0], exp, out[2]])
                transmat[concat] = len(newtransit) - 1

            else:
                newtransit[transmat[concat]][1] = '(' + newtransit[transmat[concat]][1] + '+' + exp + ')'

    gnfa['transition_function'] = newtransit[:]
    gnfa['states'] = gnfa['states'][1:]

def gnfaEdge(dfa, gnfa):
    transmat = {}
    newtransit = []

    for t in range(0, len(dfa['transition_function'])):
        transit = dfa['transition_function'][t]
        concat = ''.join(transit[0]) + ''.join(transit[2])

        if(concat in transmat):
            newtransit[transmat[concat]][1] = '(' + newtransit[transmat[concat]][1] + '+' + transit[1] + ')'

        else:
            newtransit.append(transit)
            transmat[concat] = len(newtransit) - 1

    gnfa['transition_function'] = newtransit[:]
    return gnfa

def gnfaEnd(dfa, gnfa):
    new = 'Qend'
    gnfa['states'].append(new)

    for s in range(0, len(dfa['final_states'])):
        gnfa['transition_function'].append([dfa['final_states'][s], '$', new])

    gnfa['final_states'] = [new]
    return gnfa

def gnfaStart(dfa, gnfa):
    new = 'Qstart'
    gnfa['states'].append(new)

    for s in range(0, len(dfa['start_states'])):
        gnfa['transition_function'].append([new, '$', dfa['start_states'][s]])

    gnfa['start_states'] = [new]
    return gnfa

def parse(inp):

    gnfa = inp.copy()
    gnfa = gnfaEdge(inp, gnfa)
    gnfa = gnfaStart(inp, gnfa)
    gnfa = gnfaEnd(inp, gnfa)

    while(len(gnfa['states']) > 2):
        stateRem(gnfa)

    return gnfa['transition_function'][0][1] 

def main():
    with open(sys.argv[1], "r") as file:
        inp = json.load(file)
    
    with open(sys.argv[2], "w") as file:
        json.dump({"regex":parse(inp)}, file)

if __name__ == "__main__":
    main()
