"""
DONE make this usable as a script on external data.
DONE eliminate display of internal tree structure.
DONE comment at least a little.
TODO use a better command-line argument mechanism

Sample execution:
$ python step.02.py wordsfile searchfile
"""

if __name__=="__main__":
    import sys

    argc=len(sys.argv)
    assert argc==3,'usage: %s {wordsfilename} {searchfilename}'%sys.argv[0]

    with open(sys.argv[1]) as wordsfile:
        words=wordsfile.read().split()

    tree,row,col={},1,1

    for word in words:
        root=tree
        for char in word.lower():
            root[char]=root.get(char,{}); root=root[char]
        root['']=list(set(root.get('',[])+[word]))

    with open(sys.argv[2]) as searchfile:
        field=searchfile.read()

    def find(head,branch,inclusive=False):
        char,found=field[head].lower(),False
        if char in branch:
            found=find(head+1,branch[char],inclusive)
        # If we have reached a terminal (branch.get('',False)
        # and the length of the discovered string is more than 1 (head-tail>>1
        # and there are other matching branches (inclusive)
        # or nothing further was found,
        # report find as row, col, buffer offset, string found, string matched
        found=branch.get('',False) and (head-tail)>1 and (inclusive or not found)
        if found:
            global row,col
            print '%d,%d,%d,%s,%s'%(
                    row,col,tail,field[tail:head],branch[''][0])
        return found

    for tail in xrange(len(field)):
        nl=int(field[tail]=='\n')
        row,col=row+nl,(1-nl)*(1+col)
        find(tail,tree,False)
