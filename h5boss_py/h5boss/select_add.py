import numpy as np
import h5py
import time
from h5boss.pmf import pmf
from h5boss.select import select
def select_add(infiles, infile, plates, mjds, fibers):
    '''
    add the missing (plates,mjds,fibers) from a set of input files
    to the pre-existing subset file
    Args:
        infiles : list of input filenames, or single filename
        infile : pre-existing subset file
        plates : list of plates
        mjds : list of plates
        fibers : list of fibers        
    '''


    miss, left = pmf(infile,plates,mjds,fibers)
    #add the missing one
    #print ('add the missing one')
    #print (type(miss[0]))
    miss2=miss.view(miss.dtype[0]).reshape(miss.shape+(-1,))[:,0]
    
    print ('miss2')
    print miss2
    plate = miss2[:,0]
    mjd = miss2[:,1]
    fiber = miss2[:,2]
    print plate
    print mjd
    print fiber
    select(infiles,infile,plate,mjd,fiber)
