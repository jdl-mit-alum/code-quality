#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import mmap
import pprint
import fuzzy
import re
import ujson

from pprint import pprint
from itertools import product

class ParLogSer(object):
    "Parallel Logarithmic Serial"

    vowel     = [False] * 256
    consonant = [False] * 256
    ignores   = ['of', 'in', 'for']

    def secondVowels(self, pattern):
        low  = pattern.lower()
        ords = [ord(c) for c in pattern]
        size = len(ords)
        find = 0
        while ParLogSer.consonant[ord(low[find])] and (find < size):
            find += 1
        while ParLogSer.vowel[ord(low[find])] and (find < size):
            find += 1
        while ParLogSer.consonant[ord(low[find])] and (find < size):
            find += 1
        return find

    def decimate(self, words, variants, maxlen=4):
        lenwords = len(words)
        if lenwords == 0:
            pass
        elif lenwords == 1:
            word = words[0]
            lenword = len(word)
            declist = []
            for n in xrange(min(lenword-1, maxlen)):
                variants.add(word[0:n])
        else:
            products = product([range(len(word)-1) for word in words])
            for lens in products:
                variants.add(''.join([word[0:n] for word, n in zip(word, lens)]))
        return self

    def makeScramble(self, pattern, variants):
        return self

    def makeShorten(self, pattern, variants):
        declared = pattern.split('|')
        if len(declared) >= 2:
            canonical = declared[0]  # First is canonical
            for variant in declared[1:]:  # Remainder are variants
                variants.add(variant, canonical)
        else:
            words = [
                    word for word in pattern.split()
                    if word not in ParLogSer.ignores]
            if len(words) > 1:
                # TODO acronyms
                initial = [word[0] for word in words]
                variants.add(''.join(initial))          # MIT
                variants.add(' '.join(initial))         # MIT
                variants.add('.'.join(initial)+'.')     # M.I.T.
                variants.add('. '.join(initial)+'.')    # M. I. T.
                # TODO contractions (this approach is too weak)
                short = [word[0:self.secondVowels(word)] for word in words]
                variants.add(' '.join(short))           # Mass Inst Techn
                variants.add('.'.join(short)+'.')       # Mass.Inst.Techn.
                variants.add('. '.join(short)+'.')      # Mass. Inst. Techn.
                # TODO make decimate work properly
                #self.decimate(words, variants)
                """
                Massachusetts Institute of Technology
                Mass Inst Tech
                """
        return self

    def makeConsonants(self, pattern, variants):
        variants.add(re.sub(r'[aeiou]', '', pattern, flags=re.IGNORECASE))
        return self

    def makeFuzzy(self, pattern, variants):
        variants.add(fuzzy.nysiis(pattern).lower())
        return self

    def makeLevenshtein1(self, pattern, variants):
        pattern = pattern.lower()
        letter = list(pattern)
        # single swaps
        for i in xrange(1, len(letter)):
            letter[i], letter[i-1] = letter[i-1], letter[i]
            variants.add(''.join(letter))
            letter[i], letter[i-1] = letter[i-1], letter[i]
        # TODO multiple swaps
        # single deletes
        for i in xrange(0, len(letter)):
            B, A = pattern[0:i], pattern[i:]
            variants.add(B+A[1:])
        # single duplicates
        for i in xrange(0, len(letter)):
            B, A = pattern[0:i], pattern[i:]
            variants.add(B+A[0]+A)
        return self

    def makeVariants(self, pattern):
        variants = set([pattern])
        self.makeLevenshtein1(pattern, variants)
        self.makeFuzzy(pattern, variants)
        self.makeConsonants(pattern, variants)
        #self.makeShorten(pattern, variants)
        #self.makeScramble(pattern, variants)
        longEnough = [variant for variant in variants if len(variant) > 1]
        self.variants[pattern] = ' OR '.join(longEnough)
        return longEnough

    def initPattern(self, pattern, canonical=None):
        target = canonical if canonical != None else pattern
        variants = self.makeVariants(pattern)
        for variant in variants:
            root = self.tree
            for char in variant:
                root[char] = root.get(char, {})
                root = root[char]
            temp = set(root.get('', set()))
            temp.add(target)
            root[''] = list(temp)
            #root[''].add(target)

    def ingest(self, filename):
        "file to ingest must have one pattern per line"
        try:
            with open(filename) as source:
                for line in source:
                    word = line.strip().lower();
                    self.initPattern(word)
                    self.word.add(word)
            #with open('parlogser.json', 'w') as json:
                #print>>json, ujson.dumps(self.tree)
        except:
            print 'Ingest failed:', filename
            print sys.exc_info()
        return self

    def __init__(self, dct):
        for v in 'aeiouy':
            ParLogSer.vowel[ord(v)] = True
            ParLogSer.vowel[ord(v.upper())] = True
        for c in 'bcdfghjklmnpqrstvwxz':
            ParLogSer.consonant[ord(c)] = True
            ParLogSer.consonant[ord(c.upper())] = True

        self.tree = {}
        self.word = set()
        self.variants = {}
        self.ingest(dct)
        #try:
            #with open('parlogser.json') as json:
                #print 'from json'
                #self.tree = ujson.loads(json.read())
        #except:
            #self.ingest(dct)
            #self.initUnixWords()
        #print 'show tree','+'*60
        #with open('parlogser.tree', 'w') as stream:
            #pprint.pprint(self.tree, stream=stream)
            #pprint.pprint(self.tree)
        #print 'show tree','-'*60

    def __call__(self, filename):
        #print '-'*50
        source = os.open(filename, os.O_RDONLY)
        self.memory = mmap.mmap(source, 0, prot=mmap.PROT_READ)
        self.row, self.col = 1, 1
        transup = False
        for self.anchor in xrange(self.memory.size()):
            o = ord(self.memory[self.anchor])
            if not (ParLogSer.vowel[o] or ParLogSer.consonant[o]):
                transup = False
                continue
            if transup == False:
                transup = True
                self.find(self.anchor, self.tree)
        self.memory.close()
        os.close(source)

    def find(self, anchor, tree, include = False):
        char = self.memory[anchor].lower()
        self.newline = int(char == '\n')
        self.row = self.row + self.newline
        self.col = (1 - self.newline) * (1 + self.col)
        if '' in tree:
            token = self.memory[self.anchor:anchor]
            found = tree['']
            # TODO consider non-uniques
            # Unique finds
            if len(found) == 1:
                print '%d,%d,%d,%s,%s'%(
                    self.row, self.col,
                    self.anchor,
                    self.memory[self.anchor:anchor],
                    found[0])

        if char in tree:
            self.find(anchor+1, tree[char])
        pass

    def display(self):
        pprint(self.tree)
        pprint(self.variants)
        ors = self.variants['University of Pennsylvania'.lower()]
        pprint(ors.split(' OR '))

if __name__ == "__main__":
    wrd = '/usr/share/dict/words' if (len(sys.argv) < 2) else sys.argv[1]
    pls = ParLogSer(wrd)
    pls('testdata')
    #pls.display()
