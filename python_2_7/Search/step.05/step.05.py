#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""step.05.py
Usage:
    step.05.py WORDSFILE SEARCHFILE
    step.05.py (-h | --help)
    step.05.py (--version)
Options:
    WORDSFILE                       One search term per space separated word
    SEARCHFILE                      Free text in which to search
    -h --help                       Show this screen
    --version                       Show version

DONE encapsulate for simplification
TODO docstrings

Sample execution:
$ step.05.py wordsfile searchfile
"""
class Search(dict):
    """Search encapsulates an entire mechanism for constructing/using trees.

A tree is formed from the letters of words from the wordsfile.  For example:
hacker have having hello hi histogram

Here is an example of a tree formed from the wordsfile:
{'h': {'a': {'c': {'k': {'e': {'r': {'': ['hacker']}}}},
             'v': {'e': {'': ['have']}, 'i': {'n': {'g': {'': ['having']}}}}},
       'e': {'l': {'l': {'o': {'': ['hello']}}}},
       'i': {'': ['hi'],
             's': {'t': {'o': {'g': {'r': {'a': {'m': {'': ['histogram']}}}}}}}}}}
By examination you can see the 1st line shows the letters of 'hacker'.
The 2nd line shares the first letters 'ha' but leads to 'have' and 'having'.
The 3rd line shares the first letter and leads to 'hello'.
The 4th line shares the first letter and leads to 'hi'.
The 5the line shares 'h' and 'i' and leads to 'histogram'.

By anchoring on a point in the search text and asking for matches up the tree
it is possible to identify any of the words from the wordsfile.
When this is implemented in C, C++, or assembler it is very fast indeed.
It is implemented here in python to illustrate the principles.
    """
    def __init__(self,**kw):
        "__init__ parses a command line, ingests a wordsfile, builds a tree."
        self.update(kw)
        self.tree={}
        with open(kw['WORDSFILE']) as wordsfile:
            for word in wordsfile.read().split():
                root=self.tree
                for char in word.lower():
                    root[char]=root.get(char,{}); root=root[char]
                root['']=list(set(root.get('',[])+[word]))
    def __call__(self):
        "__call__ reads the searchfile and applies the search algorithm."
        self.row,self.col=1,1
        with open(kwargs['SEARCHFILE']) as searchfile:
            self.field=searchfile.read()

        for self.tail in xrange(len(self.field)):
            nl=int(self.field[self.tail]=='\n')
            self.row,self.col=self.row+nl,(1-nl)*(1+self.col)
            self.find(self.tail,self.tree,False)
    def find(self,head,branch,inclusive=False):
        "find implements the search algorithm using the tree."
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
    "__main__ enables testing of the Search class from within the module."
    from docopt import (docopt)
    kwargs=docopt(__doc__,version="0.0.1")
    search=Search(**kwargs)
    search()
