import numpy as np
import h5py
import time,os
import traceback 
from h5boss.pmf import pmf 
from h5boss.select import select


## Global variables:
fx=""
pid=""
inputfile=""
fiberdatalink={} 
## Data structure of fiberdatalink: {key, value_pair()} --->  {path_dataset, (datatype,datashape,filename)}
## For example fiberdatalink['3665/52273/360/coadd']= (V32, $SCRATCH/h5boss/3665-52273.h5)
## Aug 3 2016
## Jialin Liu, jalnliu@lbl.gov


def traverse_node(name):
    '''
       para   : node name in a hdf5 group
       purpose: Find a dataset node, which should be an endpoint in its group hierarchy
       return : (key,value)->(path_to_dataset, dataset type) 
    '''
    global fx,pid,fiberdatalink,inputfile
    try:
     cur_node=name.encode('ascii','ignore')
     node=pid+'/'+cur_node
     node_t=str(type(fx[node]))
     if 'dataset' in node_t:
        node_t=fx[node].dtype
        node_sp=fx[node].shape
        fiberdatalink[node]=(node_t,node_sp,inputfile)
    except Exception as e:
     traceback.print_exc()
     pass      

#node_type is used in ../script/subset_mpi.py, which creates single shared large file 
def node_type(infile,plates,mjds,fibers):       
        '''
           para  : filename, plate, mjd, fiber
           return: (key, value)->(plates/mjd/fiber/../dataset, filename)
           python dict's updating can ensure that the key is unique, i.e., plate/mjd/fiber/../dataset is unique
        '''
        global pid,fiberdatalink,fx,inputfile
        inputfile=infile
        try: 
         fx = h5py.File(infile, mode='r')
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

# create_slavefile is used in ../script/subset_mpi-sf.py, which creates multiple sub files 
def create_slavefile(infile,plates,mjds,fibers,masterfile,rank,id):
    master_dir=os.path.dirname(os.path.realpath(masterfile))+'/'+os.path.basename(masterfile).split('.')[0]
     
    slavefile=master_dir+'/'+str(rank)+'_'+str(id)+'.h5'
    try:
      select(infile, slavefile, plates, mjds, fibers)
    except Exception as e:
      print ("Error in slave file:%s")
      traceback.print_exc()
      pass   
