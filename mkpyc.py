#!/usr/bin/python

import os
currpath = os.path.join(os.getcwd(), os.path.dirname(__file__))

def printfile(path):
    if os.path.exists(path):
        files = os.listdir(path)
        for f in files:
            subpath = os.path.join(path, f)
            if os.path.isdir(subpath):
                printfile(subpath)
            else:
                #print(subpath)
                if subpath.endswith(".pyc"):
                    os.system("rm -fr %s" % subpath)

if __name__ == "__main__":
    printfile(currpath)