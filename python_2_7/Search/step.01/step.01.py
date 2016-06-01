"""
Hi programmer,
You are used to writing sample programs like "hello world".
This is like a hello world for multi-pattern string search.
It is written in the primitive hacker script style.
It is run by executing "python step.01.py".
A kind of histogram of match counts is produced.
Finds with a count of 1 are emitted.
This __doc__ string is used as test text.
Having no significant quality was a goal of this code.
No serious quality metrics have been applied.
Unfortunately, having a __doc__ counts towards quality.
This code will be used as the subject for the
ordered application of quality metrics to aid in taking
early agile prototype code to late waterfall quality.
Say hi to other coders by showing them this code.
"""
words="hacker have having hello hi histogram".split()
tree,row,col={},1,1

for word in words:
    root=tree
    for char in word.lower():
        root[char]=root.get(char,{}); root=root[char]
    root['']=list(set(root.get('',[])+[word]))

def find(head,branch,inclusive=False):
    char,found=__doc__[head].lower(),False
    if char in branch:
        found=find(head+1,branch[char],inclusive)
    found = branch.get('',False) and (head-tail)>1 and (inclusive or not found)
    if found:
        global row,col
        print '%d,%d,%d,%s,%s'%(
                row,col,tail,__doc__[tail:head],branch[''][0])
    return found

for tail in xrange(len(__doc__)):
    nl=int(__doc__[tail]=='\n')
    row,col=row+nl,(1-nl)*(1+col)
    find(tail,tree,False)

from pprint import pprint

pprint(tree)
