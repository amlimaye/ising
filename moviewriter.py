#!/usr/bin/env python

import os
import sys
import matplotlib
matplotlib.use("MacOSX")
import matplotlib.pyplot

def main(args):
    directory = args[0]
    fullpath = os.path.join(os.getcwd(),directory)
    nfiles = len(os.listdir(fullpath))
    print nfiles

if __name__ == "__main__":
    main(sys.argv[1:])
