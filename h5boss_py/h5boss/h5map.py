import numpy as np
import h5py
import time
import sys
import os
import csv
import traceback
from collections import defaultdict
fx=""
pid=""
inputfile=""
fiberdatalink={}
cataloglink={}
meta=['plugmap', 'zbest', 'zline',
                        'photo/match', 'photo/matchflux', 'photo/matchpos']

def _traverse_fibernode(name):
    '''
       para   : node name in a hdf5 group
       purpose: Find a dataset node, which should be an endpoint in its group hierarchy
unique_datsetpath datasettype datasetshape filepath plate mjd fiber
       return : (key,value)->(path_to_dataset, (dataset type, shape, filename, plate, mjd, fiber)) 
    '''
    global fx,pid,fiberdatalink,inputfile
    try:
     cur_node=name.encode('ascii','ignore')
     node=pid+'/'+cur_node
     p=pid.split('/')[0]
     m=pid.split('/')[1]
     f=pid.split('/')[2]
     node_t=str(type(fx[node]))
     if 'dataset' in node_t:
        node_t=fx[node].dtype
        node_sp=fx[node].shape
        fiberdatalink[node]=(node_t,node_sp,inputfile,p,m,f)
    except Exception as e:
     traceback.print_exc()
     pass
#node_type is used in ../script/subset_mpi.py, which is to create single shared file 
def map_fiber(infile):
        '''
           para  : filename, plate, mjd, fiber
           return: (key, value)->(datapath, (dtype, shape, filename, plate, mjd, fiber))
           python dict's updating can ensure that the key is unique, i.e., datapath: plate/mjd/fiber/../dataset is unique
        '''
        global pid,fiberdatalink, cataloglink, fx, inputfile
        inputfile=infile
        try:
         fx = h5py.File(infile, mode='r')
         for plate in fx.keys():
            for mjd in fx[plate].keys():
               spid= '{}/{}'.format(plate, mjd)
               for fib in fx[spid].keys():
                   if fib.isdigit()
                   pid = '{}/{}/{}'.format(plate, mjd, fib)
                   fx[pid].visit(_traverse_fibernode)
                #for im in meta:
                #  mnode=spid+'/'+im
                #  mnode_t=fx[mnode].dtype
                #  mnode_sp=fx[mnode].shape
                #  fiberdatalink[mnode]=(mnode_t,mnode_sp,infile)
         fx.close()
        except Exception as e:
         print (pid)
         traceback.print_exc()
         print (pid,infile)
         pass
        return (fiberdatalink)
def map_pmf(infile):
        '''
           para  : filename, plate, mjd, fiber
           return: (key, value)->(plates/mjd/fiber/, filename)
           python dict's updating can ensure that the key is unique, i.e., plate/mjd/fiber/../dataset is unique
        '''
        pmf={}
        try:
         fx = h5py.File(infile, mode='r')
         for plate in fx.keys():
            for mjd in fx[plate].keys():
               spid= '{}/{}'.format(plate, mjd)
               for fib in fx[spid].keys():
                   if fib.isdigit():
                    pid = '{}/{}/{}'.format(plate, mjd, fib)
                    pmf[pid]=infile 
         fx.close()
        except Exception as e:
         print (pid)
         traceback.print_exc()
         print (pid,infile)
         pass
        return (pmf)
