#!/usr/bin/env python
"""
step.04.py
Usage:
    step.04.py WORDSFILE SEARCHFILE
    step.04.py (-h | --help)
    step.04.py (--version)
Options:
    WORDSFILE                       One search term per line
    SEARCHFILE                      Free text in which to search
    -h --help                       Show this screen
    --version                       Show version

DONE made script directly executable without "python" on command-line.
DONE use a better command-line argument mechanism
TODO encapsulate for simplification

Sample execution:
$ step.04.py wordsfile searchfile
"""
class Search(dict):
    def __init__(self,**kw):
        self.update(kw)
        self.tree={}
        with open(kw['WORDSFILE']) as wordsfile:
            for word in wordsfile.read().split():
                root=self.tree
                for char in word.lower():
                    root[char]=root.get(char,{}); root=root[char]
                root['']=list(set(root.get('',[])+[word]))
    def __call__(self):
        self.row,self.col=1,1
        with open(kwargs['SEARCHFILE']) as searchfile:
            self.field=searchfile.read()

        for self.tail in xrange(len(self.field)):
            nl=int(self.field[self.tail]=='\n')
            self.row,self.col=self.row+nl,(1-nl)*(1+self.col)
            self.find(self.tail,self.tree,False)
    def find(self,head,branch,inclusive=False):
        char,found=self.field[head].lower(),False
        if char in branch:
            found=self.find(head+1,branch[char],inclusive)
        # If we have reached a terminal (branch.get('',False)
        # and the length of the discovered string is more than 1 (head-tail>>1
        # and there are other matching branches (inclusive)
        # or nothing further was found,
        # report find as row, col, buffer offset, string found, string matched
        found=branch.get('',False) and (head-self.tail)>1 and (inclusive or not found)
        if found:
            print '%d,%d,%d,%s,%s'%(
                    self.row,self.col,self.tail,self.field[self.tail:head],branch[''][0])
        return found
if __name__=="__main__":
    from docopt import (docopt)
    kwargs=docopt(__doc__,version="0.0.1")
    search=Search(**kwargs)
    search()
