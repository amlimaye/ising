#!/usr/bin/env python -u

#import required libraries, use TkAgg backend for plotting
import numpy as np
import matplotlib
matplotlib.use("MacOSX")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os
import logger
import progressbar
from progressbar import ProgressBar
import argparse

class IsingLattice:
    #class constructor
    def __init__(self,n_x,n_y,random=False):
        if random:
            self._lattice = np.random.choice(np.array([-1,1]),size=(n_x,n_y))
        else:
            self._lattice = np.ones(n_x,n_y)

    #flip spin state at lattice site x,y
    def flip(self,x,y):
        if self._lattice[x,y] == -1:
            self._lattice[x,y] = 1;
        elif self._lattice[x,y] == 1:
            self._lattice[x,y] = -1;
        else:
            raise ValueError("Found invalid spin value at (%d,%d)"%(x,y))

    #plot lattice
    def show(self,ax):
        ax.clear()
        ax.matshow(self._lattice,cmap=plt.get_cmap("YlGnBu"))
        return ax

    #get spin state at lattice site x,y
    def get(self,x,y):
        return self._lattice[x,y]

    #get lattice shape
    def shape(self):
        return self._lattice.shape

    #return numpy representation of current lattice state
    def getNumpy(self):
        return np.array(self._lattice)

    #get neighbors for lattice site x,y
    def getNeighbors(self,x,y):
        #initialize simple nearest neighbor list
        neighborList = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        #delete off edge cases
        deletionList = []
        if x == self._lattice.shape[0]-1:
            deletionList.append(0)
        elif x == 0:
            deletionList.append(1)
        if y == self._lattice.shape[1]-1:
            deletionList.append(2)
        elif y == 0:
            deletionList.append(3)
        deletionList.sort(reverse=True)
        for idx in deletionList:
            neighborList.pop(idx)
        return neighborList

#hamiltonian evaluation function
def hamiltonian(lattice,xytuple,eps,extfield,flip=True):
    shape = lattice.shape()
    x = xytuple[0]
    y = xytuple[1]
    if flip:
        oldHamiltonian = -1*eps*sum([lattice.get(x,y)*lattice.get(neighbor[0],
                                                                  neighbor[1])
                                    for neighbor in lattice.getNeighbors(x,y)])
        lattice.flip(x,y)
        newHamiltonian = -1*eps*sum([lattice.get(x,y)*lattice.get(neighbor[0],
                                                                  neighbor[1])
                                    for neighbor in lattice.getNeighbors(x,y)])
    else:
        lattice.flip(x,y)
        oldHamiltonian = -1*eps*sum([lattice.get(x,y)*lattice.get(neighbor[0],
                                                                  neighbor[1])
                                    for neighbor in lattice.getNeighbors(x,y)])
        lattice.flip(x,y)
        newHamiltonian = -1*eps*sum([lattice.get(x,y)*lattice.get(neighbor[0],
                                                                  neighbor[1])
                                    for neighbor in lattice.getNeighbors(x,y)])
    
    #calculate external field term and add to hamiltonian
    newHamiltonian += -1*extfield*lattice.get(x,y)

    return newHamiltonian-oldHamiltonian

#metropolis move acceptance function
def metropolis(lattice,temperature,eps=1,extfield=0):
    #evaluate inverse temperature
    beta = 1/temperature
    #sample x,y point on lattice from uniform distribution over the integers
    pickedX = np.random.random_integers(0,lattice.shape()[0]-1)
    pickedY = np.random.random_integers(0,lattice.shape()[1]-1)
    #flip spin and calculate dH
    dH = hamiltonian(lattice,(pickedX,pickedY),eps,extfield,flip=True)
    #accept or reject according to metropolis function
    if (dH > 0):
        boltzmann = np.exp(-1*beta*dH)
        randNum = np.random.uniform()
        result = True
        if boltzmann <= randNum:
            lattice.flip(pickedX,pickedY)
            result = False
    else:
        boltzmann = 1
        randNum = 1
        result = True

    logdict = {"x":pickedX,"y":pickedY,"dH":dH,"met":boltzmann,"rng":randNum,
               "result":result}
    return logdict

def main(args):
    #assign arguments from command line
    n_x = args.n_x
    n_y = args.n_y
    nmoves = args.nmoves
    temperature = args.T
    logfile = args.logfile
    moviefile = args.moviefile
    eps = args.eps
    extfield = args.ext
    interval = args.interval
    location = args.moviedata_loc

    #create directory for movie data if location is provided
    if location:
        locpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),location);
        if not os.path.exists(locpath):
            os.mkdir(locpath)

    #construct ising lattice
    lattice = IsingLattice(n_x,n_y,random=True)

    #start logger if requested
    if logfile:
        keys = ['x','y','dH','met','rng','result']
        fmt = "%8d,%d,%d,%0.8f,%0.8f,%0.8f,%i"
        log = logger.MetropolisLogger(logfile,keys,fmtstring=fmt)    

    #make figure to plot matrix on
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    #start and setup animator on this figure
    if moviefile:
        FileMovieWriter = matplotlib.animation.writers['ffmpeg']
        mwriter = FileMovieWriter(fps=60)
        mwriter.setup(fig,moviefile,100)

    #print message with program start
    sys.stdout.write("Starting %d Monte Carlo moves on (%d x %d) lattice\n"
                     %(nmoves,n_x,n_y))
    #initialize a progressbar for loop
    widgets = ['Monte Carlo: ', progressbar.Percentage(), ' ', 
               progressbar.Bar(marker=progressbar.RotatingMarker()),
               ' ', progressbar.ETA(), ' ', 
               progressbar.FileTransferSpeed('iters')]
    pbar = ProgressBar(widgets=widgets, maxval=nmoves).start()
    #loop to nmoves
    for i in pbar(range(0,nmoves)):
        logdict = metropolis(lattice,temperature,eps=eps,extfield=extfield)
        if (i % interval == 0):
            if location:
                filename = 'frame%04d' % (i/interval)
                np.savez_compressed(os.path.join(locpath,filename),lattice.getNumpy())
            else:
                lattice.show(ax)
        if logfile:
            log.write_log(logdict,num=i+1)
        if moviefile:
            mwriter.grab_frame()
        pbar.update()
    pbar.finish()

    if moviefile:
        mwriter.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A Monte Carlo Ising Model "
                                                 "Simulator")
    parser.add_argument('n_x',type=int,help='Number of cells in x-direction')
    parser.add_argument('n_y',type=int,help='Number of cells in y-direction')
    parser.add_argument('T',type=float,help='Temperature to conduct simulation at')
    parser.add_argument('--eps',type=float,help='Strength of coupling interaction, default=1.0',default=1.0)
    parser.add_argument('--ext',type=float,help='Strength of external field interaction, default=0.0',default=0.0)
    parser.add_argument('-n','--nmoves',type=int,help="Number of Monte Carlo moves to execute, default: 100",
                        default=100)
    parser.add_argument('-o','--logfile',type=str,help="Name of file to write Metropolis"
                                              " log to, default=None")
    parser.add_argument('-l','--moviedata_loc',type=str,help="Name of directory to write movie data to, default=None")
    parser.add_argument('-m','--moviefile',type=str,help="Name of file to write movie to, default=None")
    parser.add_argument('-i','--interval',type=int,help="Interval to dump movie frames on, default=100",default=100)
    args = parser.parse_args()

    main(args)
