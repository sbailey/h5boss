import numpy as np
import h5py
import time
from h5boss.sql import sql
from h5boss.select import select
import traceback
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
    select(infiles,infile,to_add)
