import numpy as np
import h5py
import time
from h5boss.pmf import pmf
from h5boss.select import select
def remove(infile, plates, mjds, fibers):
    '''
    remove the additional (plates, mjds, fibers) from the pre-existing file

    Args:
        infile : pre-existing subset file
        plates : list of plates
        mjds : list of plates
        fibers : list of fibers        
    '''
    try: 
      fx=h5py.File(infile,'a')
    except Exception, e:
      print ('File open error in removing')
    try:
     k=0
     j=0
     print (len(plates))
     #plates=plates.reshape(plates.shape+(-1,))
     print plates[0]
     for i in range(0,len(plates)):
      a=str(plates[i])+'/'+str(mjds[i])+'/'+str(fibers[i])
      print a
      if a in fx:
        fx.__delitem__(a)
        k+=1
      else:
       j+=1
     print ('Removed %d pmf,Skipped %d'%k%j)
     fx.close()
    except Exception, e:
     print ('Error in removing')  
