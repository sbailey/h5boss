import numpy as np
import h5py
import time
import sys,os
import commands
from h5boss.select import select
def remove(infile, plates, mjds, fibers,repack=None):
    '''
    remove the additional (plates, mjds, fibers) from the pre-existing file

    Args:
        infile : pre-existing subset file
        plates : list of plates
        mjds : list of plates
        fibers : list of fibers        
    '''
    meta=['plugmap', 'zbest', 'zline',
                        'photo/match', 'photo/matchflux', 'photo/matchpos']
    tstart=time.time()
    try: 
      fx=h5py.File(infile,'a')
    except Exception, e:
      print ('File open error in removing')
    try:
     k=0
     j=0
     for i in range(0,len(plates)):
      a=str(plates[i])+'/'+str(mjds[i])+'/'+str(fibers[i])
      if a in fx:
        fx.__delitem__(a)
        k+=1
      else:
       j+=1
      #TODO:remove entries in photo, plugmap, etc
     print ('Removed %d plates/mjds/fibers,Skipped %d'%(k,j))
     fx.close()
    except Exception, e:
     traceback.print_exc()     
     print ('Error in removing')
    tend=time.time()-tstart
    print ("Remvoing Time: %.2f seconds"%tend)
    if repack=="yes":
      print ("Running repacking:")
      repack_start=time.time()
      #run hdf5 repack utility from 
      cmd_moduleload = "module load cray-hdf5 >/dev/null"
      oufile=infile.split('.')[0]+"_repack"+".h5"
      cmd_repack = "h5repack %s %s 2>/dev/null"%(infile,oufile)
      try: 
	commands.getstatusoutput(cmd_moduleload)
	commands.getstatusoutput(cmd_repack)
      except Exception,e:
        print ('Repack error')
      repack_end=time.time()-repack_start
      print ("Repacking Time: %.2f seconds"%repack_end)
