#!/usr/bin/env python

import os
import sys
import matplotlib
matplotlib.use("MacOSX")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def update_figure(num,directory,data_prefix):
    #grab current data from its .npz file
    currFile = os.path.join(directory,data_prefix+("%04d.npz" % (num+1)))
    data = np.load(currFile)['arr_0']

    #clear axis and replot
    im.set_data(data)

    #return image object
    return im

def main(args):
    #get directory in which movie data is being saved
    directory = args[0]
    outfile = args[1]

    #get file prefix (default for now until argparse is implemented)
    prefix = "frame"

    #count number of files in this directory
    fullpath = os.path.join(os.getcwd(),directory)
    nfiles = len(os.listdir(fullpath))

    #initialize frame counter variable
    update_figure.frame_counter = 0 

    #make figure window
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    #fetch data for first frame
    firstFile = os.path.join(directory,prefix+("%04d.npz" % 0))
    firstData = np.load(firstFile)['arr_0']
    
    #make a global variable for first frame image (clunky, but works for now)
    global im
    im = ax.imshow(firstData,cmap=plt.get_cmap('YlGnBu'),interpolation='none')
    
    #make animation
    movie = animation.FuncAnimation(fig,update_figure,fargs=(directory,prefix),frames=nfiles-1,interval=20,blit=True)

    #initialize filewriter and write movie to file
    MovieWriter = animation.writers['ffmpeg']
    mwriter = MovieWriter(fps=60)
    movie.save("%s.mp4" % outfile, writer=mwriter)

if __name__ == "__main__":
    main(sys.argv[1:])
