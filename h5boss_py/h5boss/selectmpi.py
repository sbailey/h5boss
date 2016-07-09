import numpy as np
import h5py
import time
import traceback 
from mpi4py import MPI

def select(infile,plates,mjds,fibers):       
        try: 
         fx = h5py.File(infile, mode='r')
	 # (kev,value) dictionary for caching (plates/mjd/fiber, filename)
         # python dict's updating can ensure that the key is unique, i.e., plate/mjd/fiber is unique
         fiberlink={}
         for plate in fx.keys():
            for mjd in fx[plate].keys():
                ii = (plates == plate) & (mjds == mjd)
                xfibers = fibers[ii]
                parent_id='{}/{}'.format(plate, mjd)
                if np.any(ii):# fiber exists
	          for fiber in xfibers:
                      id = '{}/{}/{}'.format(plate, mjd, fiber)                      
                      fiberlink={id:infile}
         fx.close()          
        except Exception as e:
         print ("File open error: %s "%infile)
        finally:
         pass
        return (fiberlink)

