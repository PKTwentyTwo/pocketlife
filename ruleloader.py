'''Handles the parsing of custom rules.'''
import os
import math
import copy
import random
import itertools
import time
try:
    from hensel import *
except ImportError:
    from .hensel import *
f = open('LifeHistory.rule', 'r')
sampletable = f.read()
f.close()
def istransition(line, knownvars={}):
    '''Determines whether a line is likely to be specifying a transition.'''
    characters = [x for x in knownvars]
    characters += [' ', ',']
    characters += [str(x) for x in range(10)]
    for n in line:
        if n not in characters:
            return False
    if line.count(',') != 9:
        return False
    return True
def parsetable(table):
    '''Parses a ruletable.'''
    lines = table.split('\n')
    name = 'testrule'
    section = 'NONE'
    globalvars = {'n_states':2, 'neighborhood':'Moore','symmetries':'permute'}
    statevars = {}
    transitions = []
    linenum = -1
    try:
        for x in lines:
            linenum += 1
            if x == '':
                #Empty line: skip
                continue
            if x[0] == '#':
                #Comment line, skip.
                continue
            if x[0] == '@':
                #Line specifies a property or section
                if ' ' in x:
                    propertyname = x[1:x.find(' ')]
                else:
                    propertyname = x[1:]
                section = propertyname
                if propertyname == 'RULE':
                    name = x[x.find(' '):].replace(' ', '')
                continue
            if section in ['ICONS', 'COLORS']:
                #Don't worry about these.
                continue
            if x.count(':') == 1 and section not in ['NONE', 'RULE', 'ICONS', 'COLORS'] :
                #Global variable line, probably.
                splitline = x.split(':')
                varname = splitline[0]
                value = splitline[1]
                if varname == 'neighborhood' and value.lower().replace(' ', '') != 'moore':
                    raise ValueError('A Lifetree can only simulate Moore neighbourhood rules.')
                globalvars[varname] = value
                continue
            if x.startswith('var') and section in ['TREE', 'TABLE']:
                #State variable. These need to be used when generating the iteration set.
                varname = x[x.find(' ')+1:x.find('=')].replace(' ', '')
                statetext = x[x.find('{')+1:x.find('}')]
                statevalues = statetext.split(',')
                statevars[varname] = statevalues
                continue
            if istransition(x, statevars):
                #Transition specification detected.
                line = x.replace(' ', '')
                spec = line.split(',')
                transitions.append(spec)
                if len(spec) != 10:
                    raise ValueError('Error on line ' + str(linenum) + ': Did not specify 10 states.')
                continue
    except Exception as e:
        raise ValueError('The following error occurred on line ' + str(linenum) + ':\n' + str(e))
    generateruleset(globalvars, statevars, transitions)
def rotate(t):
    '''Rotates a set of states 90* clockwise.'''
    m = t[1:9]
    newouter = [m[6], m[7], m[0], m[1], m[2], m[3], m[4], m[5]]
    new = t[0] + newouter + t[9]
    return new
def reflect(t):
    '''Reflects a set of states in the x axis.'''
    m = t[1:9]
    newouter = [m[4], m[3], m[2], m[1], m[0], m[7], m[6], m[5]]
    new = t[0] + newouter + t[9]
    return new
def permute(transition):
    '''Permutes a transition.'''
    modify = transition[1:9]
    arrangements = list(itertools.permutations(modify))
    arrangements = [[transition[0]] + list(x) + [transition[9]] for x in arrangements]
    present = set()
    removed = 0
    #Remove duplicates:
    for x in range(40320):
        item = arrangements[x - removed]
        if ''.join(item) not in present:
            present.add(''.join(item))
        else:
            arrangements.pop(x - removed)
            removed += 1
    return arrangements
def rotate8(transition):
    '''Applies the needed operations to a transition to apply rotate8.'''
    modify = transition[1:9]
    retval = []
    for x in range(8):
        newarrangement = []
        for n in range(8):
            newarrangement.append(modify[(n+x)%8])
        retval.append([transition[0]] + newarrangement + [transition[9]])
    return retval
def getorientations(transition, symmetry):
    '''Returns a list of the different orientations of a transition.'''
    if symmetry == 'none':
        return [transition]
    if symmetry == 'permute':
        return permute(transition)
    if symmetry == 'rotate4reflect':
        orientations = []
        for a in range(2):
            for b in range(4):
                transition = rotate(transition)
                if transition not in orientations:
                    orientations.append(transition)
            transition = reflect(transition)
        return orientations
    if symmetry == 'rotate8':
        return rotate8(transition)
    if symmetry == 'rotate4':
        orientations = []
        for b in range(4):
            transition = rotate(transition)
            if transition not in orientations:
                orientations.append(transition)
            transition = reflect(transition)
        return orientations
    return getorientations(transition, 'none')      
def generateruleset(globalvars, statevars, transitions):
    '''Generates a dictionary used to iterate a custom rule.'''
    #Note to self: Apply transformations, THEN variables. Not the other way around.
    #This function is REALLY slow - the result has to be cached.
    starttime = time.time()
    rulesetdict = {}
    powerdiff = math.floor(math.log2(int(globalvars['n_states']))) + 1
    processed = 0
    for t in transitions:
        processed += 1
        print('Now processing: '+str(processed)+'/'+str(len(transitions)))
        usedvars = []
        for x in t:
            if not x.isnumeric():
                if x not in usedvars:
                    usedvars.append(x)
        ranges = {x:statevars[x] for x in usedvars}
        uniquevals = iterate(ranges)
        transformations = getorientations(t, globalvars['symmetries'])
        print('Processing '+str(len(transformations))+' transformations and '+str(len(uniquevals))+' variable values...')
        total = 0
        for x in transformations:
            
            oglist = copy.deepcopy(x)
            for y in uniquevals:
                newlist = copy.deepcopy(oglist)
                pos = -1
                for n in newlist:
                    pos += 1
                    if n in y:
                        newlist[pos] = y[n]
                rulesetdict[intify(newlist, powerdiff)] = newlist[-1]
                total += 1
                if total%1000000 == 0:
                    print(str(total)+'/'+str(len(transformations) * len(uniquevals))+' combinations applied...')
    print('Successfully compiled rule in '+str(time.time() - starttime)+' seconds.')
    return rulesetdict
def intify(transition, powerdiff=1):
    '''Turns a transition into an integer so that it can be saved.'''
    integer = 0
    transition = [int(x) for x in transition]
    integer += transition[0] * (2**(4*powerdiff))
    integer += transition[1] * (2**(7*powerdiff))
    integer += transition[2] * (2**(6*powerdiff))
    integer += transition[3] * (2**(3*powerdiff))
    integer += transition[4] * (2**(0*powerdiff))
    integer += transition[5] * (2**(1*powerdiff))
    integer += transition[6] * (2**(2*powerdiff))
    integer += transition[7] * (2**(5*powerdiff))
    integer += transition[8] * (2**(8*powerdiff))
    return integer

def iterate(variables):
    '''Returns a list of dictionaries that can be used to iterate over all possibilities for a variable.'''
    if len(variables) == 0:
        return []
    retval = []
    totalpos = 1
    varnames = [x for x in variables]
    for x in variables:
        totalpos *= len(variables[x])
    divvals = {}
    modvals = {}
    for v in varnames:
        index = varnames.index(v)
        divval = 1
        for x in range(index+1, len(varnames)):
            divval *= len(variables[varnames[x]])
        divvals[v] = divval
        modvals[v] = len(variables[v])
    for t in range(totalpos):
        valdict = {}
        for v in varnames:
            valdict[v] = (t//divvals[v])%modvals[v]
        retval.append(valdict)
    return retval
parsetable(sampletable)
