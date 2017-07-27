import numpy as np
import h5py
import time
import traceback
from h5boss.sql import sql 
from h5boss.select import select
from h5boss.remove import remove
def select_update(infiles, infile, pmflist,repack=None):
    '''
    add the missing (plates,mjds,fibers) from a set of input files
    to the pre-existing subset file
    remove the additional (plates, mjds, fibers) from the pre-existing file

    Args:
        infiles : list of input filenames, or single filename
        infile : pre-existing subset file
        plates : list of plates
        mjds : list of plates
        fibers : list of fibers        
    '''
    to_add=[]
    to_del=[]
    try:
     to_add, to_del = sql(infile,pmflist)
    except Exception, e:
     print ('Metadata query error')
     traceback.print_exc()

    add_plates=[i.split(' ')[0] for i in to_add]
    add_mjds=[i.split(' ')[1] for i in to_add]
    add_fibers=[i.split(' ')[2] for i in to_add]
    del_plates=[i.split(' ')[0] for i in to_del]
    del_mjds=[i.split(' ')[1] for i in to_del]
    del_fibers=[i.split(' ')[2] for i in to_del]

    try:
     print ('plates/mjds/fibers to be added: %d'%len(add_plates))
     if len(add_plates)>0:
      print ("Running selection:")
      select(infiles,infile,add_plates,add_mjds,add_fibers)
    except Exception, e:
      print ('Error in adding new pmf to the file:%s'%infile)

    try:
      print ('plates/mjds/fibers to be removed: %d'%len(del_plates))
      if len(del_plates)>0:
       print ("Running removing:")
       remove(infile, del_plates,del_mjds,del_fibers,repack) 
    except Exception, e:
      print ('Error in removing pmf in the file:%s'%infile)

