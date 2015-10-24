#!/usr/bin/env python -u

#import required libraries, use TkAgg backend for plotting
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import sys

class IsingLattice:
    #class constructor
    def __init__(self,n_x,n_y,random=False):
        if random:
            self._lattice = np.random.choice(np.array([-1,1]),size=(n_x,n_y))
        else:
            self._lattice = np.ones(n_x.n_y)
    
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
        plt.draw()
        return ax

    #get spin state at lattice site x,y
    def get(self,x,y):
        return self._lattice[x,y]

    #get lattice shape
    def shape(self):
        return self._lattice.shape

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
def hamiltonian(lattice,eps=1):
    shape = lattice.shape()
    hamiltonian = 0
    for i in range(0,shape[0]):
        for j in range(0,shape[1]):
            hamiltonian += -1*eps*sum([lattice.get(i,j)*lattice.get(neighbor[0],neighbor[1]) for neighbor in lattice.getNeighbors(i,j)])
    return hamiltonian

#metropolis move acceptance function
def metropolis(lattice,temperature):
    #evaluate inverse temperature
    beta = 1/temperature
    #calculate original hamiltonian
    origHamiltonian = hamiltonian(lattice)
    #sample x,y point on lattice from uniform distribution over the integers
    pickedX = np.random.random_integers(0,lattice.shape()[0]-1)
    pickedY = np.random.random_integers(0,lattice.shape()[1]-1)
    #flip spin at the picked lattice point
    lattice.flip(pickedX,pickedY)
    #calculate new hamiltonian under lattice with flipped spin
    newHamiltonian = hamiltonian(lattice)
    #accept or reject according to metropolis function
    if (newHamiltonian-origHamiltonian > 0):
        boltzmann = np.exp(-1*beta*(newHamiltonian-origHamiltonian))
        randNum = np.random.uniform()
        if boltzmann <= randNum:
            lattice.flip(pickedX,pickedY)
            sys.stdout.write("Rejected Metropolis move at (%d,%d); Probability: %0.4f\n" % (pickedX,pickedY,boltzmann))
        else:
            sys.stdout.write("Accepted Metropolis move at (%d,%d); Probability: %0.4f\n" % (pickedX,pickedY,boltzmann))
    else:
        sys.stdout.write("Accepted Metropolis move at (%d,%d); Probability: 1\n" % (pickedX,pickedY))

def main(args):
    #assign arguments from command line
    n_x =  int(args[0])
    n_y = int(args[1])
    nmoves = int(args[2])
    temperature = float(args[3])
    #construct ising lattice
    lattice = IsingLattice(n_x,n_y,random=True)
    #apply monte carlo moves
    sys.stdout.write("Starting %d Monte Carlo moves on (%d x %d) lattice\n"%(nmoves,n_x,n_y))
    #make figure to plot matrix on
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for i in range(0,nmoves):
        metropolis(lattice,temperature)
        lattice.show(ax)
    plt.savefig("last.png")

if __name__ == "__main__":
    main(sys.argv[1:])
