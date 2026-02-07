'''Handles the parsing of custom rules.'''
import os
import math
import copy
import itertools
try:
    from hensel import *
except:
    from .hensel import *
sampletable = '''@RULE LifeHistory

A variant of HistoricalLife with two extra ON states
and two extra OFF states, for annotation purposes:

state 0:  OFF
state 1:  ON
state 2:  history/envelope (state=2 if cell was ever ON)
state 3:  marked ON (may change to OFF but will always remain marked)
state 4:  marked OFF (may change to ON but will always remain marked)
state 5:  start ON (becomes a normal marked OFF cell when it dies)
state 6:  boundary OFF (can never turn on -- can keep subpatterns in a
          stamp collection from interfering with each other)

@TABLE

n_states:7
neighborhood:Moore
symmetries:rotate8

var a={0,2,4,6}
var b={0,2,4,6}
var c={0,2,4,6}
var d={0,2,4,6}
var e={0,2,4,6}
var f={0,2,4,6}
var g={3,5}
var h={0,1,2}
var i={0,1,2,3,4,5,6}
var j={0,1,2,3,4,5,6}
var k={0,1,2,3,4,5,6}
var l={0,1,2,3,4,5,6}
var m={0,1,2,3,4,5,6}
var n={0,1,2,3,4,5,6}
var o={0,1,2,3,4,5,6}
var p={0,1,2,3,4,5,6}
var q={1,3,5}
var R={1,3,5}
var S={1,3,5}
var T={1,3,5}
var u={3,4,5}

# boundary cell always stays a boundary cell
6,i,j,k,l,m,n,o,p,6

# anything else that touches a boundary cell dies
# (using 'u' instead of 'g' below lets gliders survive as blocks)
g,6,i,j,k,l,m,n,o,4
1,6,i,j,k,l,m,n,o,2

# marked 3-neighbour birth
#  (has to be separate from the next section
#   only to handle the extra 'start' state 5)
4,R,S,T,a,b,c,d,e,3
4,R,S,a,T,b,c,d,e,3
4,R,S,a,b,T,c,d,e,3
4,R,S,a,b,c,T,d,e,3
4,R,S,a,b,c,d,T,e,3
4,R,a,S,b,T,c,d,e,3
4,R,a,S,b,c,T,d,e,3

# marked 3-neighbour survival
g,R,S,T,a,b,c,d,e,g
g,R,S,a,T,b,c,d,e,g
g,R,S,a,b,T,c,d,e,g
g,R,S,a,b,c,T,d,e,g
g,R,S,a,b,c,d,T,e,g
g,R,a,S,b,T,c,d,e,g
g,R,a,S,b,c,T,d,e,g

# normal 3-neighbour birth
h,R,S,T,a,b,c,d,e,1
h,R,S,a,T,b,c,d,e,1
h,R,S,a,b,T,c,d,e,1
h,R,S,a,b,c,T,d,e,1
h,R,S,a,b,c,d,T,e,1
h,R,a,S,b,T,c,d,e,1
h,R,a,S,b,c,T,d,e,1

# 2-neighbour survival
q,R,S,a,b,c,d,e,f,q
q,R,a,S,b,c,d,e,f,q
q,R,a,b,S,c,d,e,f,q
q,R,a,b,c,S,d,e,f,q

# ON states 3 and 5 go to history state 4 if they don't survive
g,i,j,k,l,m,n,o,p,4

# Otherwise ON states die and become the history state
q,i,j,k,l,m,n,o,p,2

@COLORS

1    0  255    0
2    0    0  128
3  216  255  216
4  255    0    0
5  255  255    0
6   96   96   96

@ICONS

XPM
/* width height num_colors chars_per_pixel */
"31 186 5 1"
/* colors */
". c #000000"
"B c #404040"
"C c #808080"
"D c #C0C0C0"
"E c #FFFFFF"
/* icon for state 1 */
"..............................."
"..............................."
"..........BCDEEEEEDCB.........."
".........CEEEEEEEEEEEC........."
".......BEEEEEEEEEEEEEEEB......."
"......DEEEEEEEEEEEEEEEEED......"
".....DEEEEEEEEEEEEEEEEEEED....."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
".....DEEEEEEEEEEEEEEEEEEED....."
"......DEEEEEEEEEEEEEEEEED......"
".......BEEEEEEEEEEEEEEEB......."
".........CEEEEEEEEEEEC........."
"..........BCDEEEEEDCB.........."
"..............................."
"..............................."
/* icon for state 2 */
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
/* icon for state 3 */
"..............................."
"..............................."
"..........BCDEEEEEDCB.........."
".........CEEEEEEEEEEEC........."
".......BEEEEEEEEEEEEEEEB......."
"......DEEEEEEEEEEEEEEEEED......"
".....DEEEEEEEEEEEEEEEEEEED....."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
".....DEEEEEEEEEEEEEEEEEEED....."
"......DEEEEEEEEEEEEEEEEED......"
".......BEEEEEEEEEEEEEEEB......."
".........CEEEEEEEEEEEC........."
"..........BCDEEEEEDCB.........."
"..............................."
"..............................."
/* icon for state 4 */
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
/* icon for state 5 */
"..............................."
"..............................."
"..........BCDEEEEEDCB.........."
".........CEEEEEEEEEEEC........."
".......BEEEEEEEEEEEEEEEB......."
"......DEEEEEEEEEEEEEEEEED......"
".....DEEEEEEEEEEEEEEEEEEED....."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
".....DEEEEEEEEEEEEEEEEEEED....."
"......DEEEEEEEEEEEEEEEEED......"
".......BEEEEEEEEEEEEEEEB......."
".........CEEEEEEEEEEEC........."
"..........BCDEEEEEDCB.........."
"..............................."
"..............................."
/* icon for state 6 */
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."

XPM
/* width height num_colors chars_per_pixel */
"15 90 5 1"
/* colors */
". c #000000"
"B c #404040"
"C c #808080"
"D c #C0C0C0"
"E c #FFFFFF"
/* icon for state 1 */
"..............."
"....BDEEEDB...."
"...DEEEEEEED..."
"..DEEEEEEEEED.."
".BEEEEEEEEEEEB."
".DEEEEEEEEEEED."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".DEEEEEEEEEEED."
".BEEEEEEEEEEEB."
"..DEEEEEEEEED.."
"...DEEEEEEED..."
"....BDEEEDB...."
"..............."
/* icon for state 2 */
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
/* icon for state 3 */
"..............."
"....BDEEEDB...."
"...DEEEEEEED..."
"..DEEEEEEEEED.."
".BEEEEEEEEEEEB."
".DEEEEEEEEEEED."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".DEEEEEEEEEEED."
".BEEEEEEEEEEEB."
"..DEEEEEEEEED.."
"...DEEEEEEED..."
"....BDEEEDB...."
"..............."
/* icon for state 4 */
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
/* icon for state 5 */
"..............."
"....BDEEEDB...."
"...DEEEEEEED..."
"..DEEEEEEEEED.."
".BEEEEEEEEEEEB."
".DEEEEEEEEEEED."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".DEEEEEEEEEEED."
".BEEEEEEEEEEEB."
"..DEEEEEEEEED.."
"...DEEEEEEED..."
"....BDEEEDB...."
"..............."
/* icon for state 6 */
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"

XPM
/* width height num_colors chars_per_pixel */
"7 42 6 1"
/* colors */
". c #000000"
"B c #404040"
"C c #808080"
"D c #C0C0C0"
"E c #FFFFFF"
"F c #E0E0E0"
/* icon for state 1 */
".BFEFB."
"BEEEEEB"
"FEEEEEF"
"EEEEEEE"
"FEEEEEF"
"BEEEEEB"
".BFEFB."
/* icon for state 2 */
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
/* icon for state 3 */
".BFEFB."
"BEEEEEB"
"FEEEEEF"
"EEEEEEE"
"FEEEEEF"
"BEEEEEB"
".BFEFB."
/* icon for state 4 */
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
/* icon for state 5 */
".BFEFB."
"BEEEEEB"
"FEEEEEF"
"EEEEEEE"
"FEEEEEF"
"BEEEEEB"
".BFEFB."
/* icon for state 6 */
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"'''
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
    retval = []
    if symmetry == 'none':
        retval.append(transition)
        return retval
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
        
        
        
def generateruleset(globalvars, statevars, transitions):
    '''Generates a dictionary used to iterate a custom rule.'''
    rulesetdict = {}
    powerdiff = math.floor(math.log2(int(globalvars['n_states']))) + 1
    for t in transitions:
        print(t)
        print(len(permute(t)))
        continue
        print(t)
        usedvars = []
        for x in t:
            if not x.isnumeric():
                #Variable detected.
                if x not in usedvars:
                    usedvars.append(x)
        ranges = {x:statevars[x] for x in usedvars}
        uniquevals = iterate(ranges)
        
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
