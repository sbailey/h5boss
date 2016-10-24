import numpy as np
import h5py
import time
from h5boss.sql import sql
from h5boss.select import select
import traceback
import os,sys
def select_add(infiles, infile, pmflist):
    '''
    add the missing (plates,mjds,fibers) from a set of input files
    to the pre-existing subset file
    Args:
        infiles : list of input filenames, or single filename
        infile : pre-existing subset file
        pmflist : list of [plate, mjd, fiber]        
    '''

    to_add, to_del = sql(infile,pmflist)
    if len(to_add)==0: 
      print ("nothing to be added")
      sys.exit()
    #split the `to_add` set into `plate` `mjd` `fiber` lists
    plates=[i.split(' ')[0] for i in to_add]
    mjds=[i.split(' ')[0] for i in to_add]
    fibers=[i.split(' ')[0] for i in to_add]
    print ("len of plates:%d"%(len(plates)))
    print ("plates:",plates)
    select(infiles,infile,plates,mjds,fibers)
