import sys
import json
import numpy as np
import time
stateCtr = -1
eps = '$'

def distinguish(s1, s2, p, tr, dfa):
    for a in range(0, len(dfa['letters'])):
        cat1 = ''.join(s1) + ''.join(dfa['letters'][a])
        cat2 = ''.join(s2) + ''.join(dfa['letters'][a])
        f1 = tr[cat1]
        f2 = tr[cat2]

        for ind in range(0, len(p)):
            if(f1 in p[ind] and f2 not in p[ind]):
                return True 
            elif(f1 in p[ind] and f2 in p[ind]):
                break

    return False

def partition(p, tr, dfa):
    newp = []

    for i in range(0, len(p)):
        temp = []

        for j in range(1, len(p[i])):
            if(distinguish(p[i][0], p[i][j], p, tr, dfa)):
                flag = False

                for k in range(0, len(temp)):
                    if(not distinguish(temp[k][0], p[i][j], p, tr, dfa)):
                        temp[k].append(p[i][j])
                        flag = True
                        break

                if(not flag):
                    temp.append([p[i][j]])

        for j in range(0, len(temp)):
            newp.append(temp[j])

            for k in range(0, len(temp[j])):
                p[i].remove(temp[j][k])

        newp.append(p[i])

    p = newp[:]
    return newp[:]

def traverse(s, transdict, newStates):
    if(s not in newStates):
        newStates.append(s)

    else:
        return 

    cat = ''.join(s)
    if(cat not in transdict):
        return

    for ind in range(0, len(transdict[cat])):
        traverse(transdict[cat][ind], transdict, newStates)

def unreach(dfa):
    transdict = {}
    newStates = []
    newtransit = []
    newfin = []

    for t in range(0, len(dfa['transition_function'])):
        transit = dfa['transition_function'][t]
        cat = ''.join(transit[0])

        if(transit[0] == transit[2]):
            continue

        if(cat in transdict and transit[2] not in transdict[cat]): 
            transdict[cat].append(transit[2])

        elif(cat not in transdict):
            transdict[cat] = [transit[2]]

    for s in range(0, len(dfa['start_states'])):
        traverse(dfa['start_states'][s], transdict, newStates)

    for t in range(0, len(dfa['transition_function'])):
        transit = dfa['transition_function'][t]

        if(transit[0] in newStates):
            newtransit.append(transit)

    for s in range(0, len(dfa['final_states'])):
        if(dfa['final_states'][s] in newStates):
            newfin.append(dfa['final_states'][s])

    dfa['states'] = newStates[:]
    dfa['transition_function'] = newtransit[:]
    dfa['final_states'] = newfin[:]

    return dfa

def parse(dfa):

    dfa = unreach(dfa)

    diff = []
    for s in range(0, len(dfa['states'])):
        if(dfa['states'][s] not in dfa['final_states']):
            diff.append(dfa['states'][s])

    prev = []
    p = [dfa['final_states'][:], diff]

    transdict = {}
    for t in range(0, len(dfa['transition_function'])):
        transit = dfa['transition_function'][t]
        cat = ''.join(transit[0]) + ''.join(transit[1])
        transdict[cat] = transit[2]

    while(prev != p):
        prev = p[:]
        p = partition(p, transdict, dfa)

    opdfa = {
            'states': p[:],
            'letters': dfa['letters'][:],
            'transition_function': [],
            'start_states': [],
            'final_states': [],
    }

    for ind in range(0, len(p)):
        for s in dfa['start_states']:
            if(s in p[ind] and p[ind] not in opdfa['start_states']):
                opdfa['start_states'].append(p[ind])

        for s in dfa['final_states']:
            if(s in p[ind] and p[ind] not in opdfa['final_states']):
                opdfa['final_states'].append(p[ind])

        for a in dfa['letters']:
            cat = ''.join(p[ind][0]) + ''.join(a)

            for x in p:
                if(transdict[cat] in x):
                    opdfa['transition_function'].append([p[ind], a, x[:]])
                    break

    return opdfa

def main():
    with open(sys.argv[1], "r") as file:
        inp = json.load(file)
    
    with open(sys.argv[2], "w") as file:
        json.dump(parse(inp), file, indent = 2)

if __name__ == "__main__":
    main()
