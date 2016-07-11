import numpy as np
import h5py
import time,os
import traceback 
from h5boss.pmf import pmf 
from h5boss.select import select
fx=""
fiberdatalink={}
pid=""
def traverse_node(name):
    global fx,pid,fiberdatalink
    try:
     cur_node=name.encode('ascii','ignore')
     node=pid+'/'+cur_node
     node_t=str(type(fx[node]))
     if 'dataset' in node_t: # this means we find a dataset node, which must be an endpoint in its group hierarchy, we don't need to record the group information, as the path to the dataset already contains path to the groups.
        node_t=fx[node].dtype
        fiberdatalink[node]=node_t
    except Exception as e:
     traceback.print_exc()
     pass       
def pmf_3(infile,plates,mjds,fibers):       
        global pid,fiberdatalink,fx
        try: 
         fx = h5py.File(infile, mode='r')
	 # (kev,value) dictionary for caching (plates/mjd/fiber, filename)
         # python dict's updating can ensure that the key is unique, i.e., plate/mjd/fiber/../dataset is unique
         fiberlink={}
         for plate in fx.keys():
            for mjd in fx[plate].keys():
                ii = (plates == plate) & (mjds == mjd)
                xfibers = fibers[ii]
                if np.any(ii): # fiber is found
	          for fiber in xfibers:#for each fiber node, recursively visit its members and record the 
                      #fiberlink={id:infile}
                      pid = '{}/{}/{}'.format(plate, mjd, fiber)                      
                      fx[pid].visit(traverse_node)  
         fx.close()          
        except Exception as e:
         print (pid)
         traceback.print_exc()
         print (pid,infile)
         pass
        return (fiberdatalink)
def create_slavefile(infile,plates,mjds,fibers,masterfile,rank,id):
    master_dir=os.path.dirname(os.path.realpath(masterfile))+'/'+os.path.basename(masterfile).split('.')[0]
     
    slavefile=master_dir+'/'+str(rank)+'_'+str(id)+'.h5'
    try:
      select(infile, slavefile, plates, mjds, fibers)
    except Exception as e:
      print ("Error in slave file:%s")
      traceback.print_exc()   
