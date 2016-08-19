#!/usr/bin/env python
"""
Create an HDF5 file from BOSS data

TODO:
  - include comments in meta/attrs
  - platelist quantities
"""
from __future__ import division, print_function
#from __future__ import absolute_import
from mpi4py import MPI
import h5py
from h5boss.pmf import parse_csv
from h5boss.pmf import get_fiberlink
from h5boss.pmf import get_catalogtypes
from h5boss.pmf import count_unique

from h5boss.selectmpi import add_dic
from h5boss.selectmpi import create_template
from h5boss.selectmpi import overwrite_template

import sys,os
import time
import optparse
import csv
import traceback
#import pandas as pd
import numpy as np
import optparse
import argparse
import datetime
from collections import defaultdict
def parallel_select():
    '''
    Select a set of (plates,mjds,fibers) from the realesed BOSS data in HDF5 formats.
    
    Args:
        input:   HDF5 files list, i.e., source data, [csv file]
        output:  HDF5 file, to be created or updated
        pmf: Plates/mjds/fibers numbers to be quried, [csv file]
       
    '''
    parser = argparse.ArgumentParser(prog='subset_mpi')
    parser.add_argument("input",  help="HDF5 input list")
    parser.add_argument("output", help="HDF5 output")
    parser.add_argument("pmf",    help="Plate/mjd/fiber list")
    parser.add_argument("--template", help="Create template only,yes/no")
    parser.add_argument("--mpi", help="using mpi yes/no")
    opts=parser.parse_args()

    infiles = opts.input
    outfile = opts.output
    pmflist = opts.pmf
    catalog_meta=['plugmap', 'zbest', 'zline',
                        'match', 'matchflux', 'matchpos']
    meta=['plugmap', 'zbest', 'zline',
                        'photo/match', 'photo/matchflux', 'photo/matchpos']
    if opts.template is None or opts.template=="no":
       template=0
    elif opts.template and opts.template=="yes":
       template=1
    if opts.mpi is None or opts.mpi=="no": 
        #starts seirial processing
        print ("Try the subset.py or subset command")
        sys.exit()
    elif opts.mpi and opts.mpi=="yes":
        comm =MPI.COMM_WORLD
        nproc = comm.Get_size()
        rank = comm.Get_rank()
        (plates,mjds,fibers,hdfsource) = parse_csv(infiles, outfile, pmflist,rank)
        tstart=MPI.Wtime()
        if rank==0: print ("Number of processes %d"%nproc)
        total_files=len(hdfsource)
        #distribute the workload evenly to each process
        step=int(total_files / nproc)+1
        rank_start =int( rank * step)
        rank_end = int(rank_start + step)
        if(rank==nproc-1):
            rank_end=total_files # adjust the last rank's range
            if rank_start>total_files:
             rank_start=total_files
        range_files=hdfsource[rank_start:rank_end]
############# GET ALL INFO NEEDED IN CREATING THE TEMPLATE ############
        fiber_dict={}
        for i in range(0,len(range_files)):
            fiber_item = get_fiberlink(range_files[i],plates,mjds,fibers)
            if len(fiber_item)>0:
             fiber_dict.update(fiber_item)      
        tend=MPI.Wtime()
        if rank==0: 
         print ("Get all nodes metadata (dataset, (type,filename)) time: %.2f"%(tend-tstart))
        #rank0 create all, then close an reopen.-Quincey Koziol 
        counterop = MPI.Op.Create(add_dic, commute=True) #define reduce operation
        global_fiber={}#(key, value)->(plates/mjd/fiber/../dataset, (type,shape,filename), unordered
        #TODO: SCAN ALL FILES, GET THE (PMF, FILE) LIST, SAVE AS PICKLE, THEN EACH TIME, READIN THIS FILE. 
        #TODO: Given PMF Query, check the PICKLE, return (PMF, FILE)
        #TODO: even though we can sort input query list, but for load balance, each rank probably still have overlapped access at file level
        #TODO: after get the metadata, may need to allreduce and then convert the dictionary into ordered list, and sort again
        fiber_item_length=len(fiber_dict)
        fiber_dict_tmp=fiber_dict
        global_fiber= comm.allreduce(fiber_dict_tmp, op=counterop)       
        treduce=MPI.Wtime()
        
        if rank==0 and template==1:
           try:
            ##can not parallel create metadata is really painful. 
            create_template(outfile,global_fiber,'fiber')
            catalog_number=count_unique(global_fiber) #(plates/mjd, num_fibers)
            print ('number of unique fibers:%d '%len(catalog_number))
            for fk,vk in catalog_number.items():
               print ("%s:%d"%(fk,vk))
            sample_file=range_files[0]
            catalog_types=get_catalogtypes(sample_file) # dict: meta, (type, shape) 
           
            global_catalog=(catalog_number,catalog_types)
            create_template(outfile,global_catalog,'catalog')
           except Exception as e:
            traceback.print_exc()
        tcreated=MPI.Wtime()
        if rank==0 and template==1:
         print ("Template creation time: %.2f"%(tcreated-treduce))
         with open('nodes10k.txt', 'a') as f:
           f.writelines('{}:{}\n'.format(k,v[2]) for k, v in global_fiber.items())
           f.write('\n')
############# OVERWRITE THE TEMPLATE WITH ACTUAL DATA ############
        if template ==0: 
         try: 
          hx = h5py.File(outfile,'a',driver='mpio', comm=MPI.COMM_WORLD) ## collectively open file 
          hx.atomic=False 
         except Exception as e:
          traceback.print_exc()        
        topen=MPI.Wtime()
        tclose=0.0
        tcopy=0.0
        if template==0:
           overwrite_template(hx,fiber_dict,'fiber')
           #for each fiber, find the catalog, then copy it
           overwrite_template(hx,fiber_dict,'catalog')
           hx.close()
           tclose=MPI.Wtime()
           #if rank==0: 
           #   overwrite_template(outfile,global_dict,'catalog')
        tcopy=MPI.Wtime()
#        try:
#           if template==0:
#            hx.close()
#        except Exception as e:
#           traceback.print_exc()
#           pass
#        tclose=MPI.Wtime()
#        if rank==0:
#           print ("Allreduce %d kv(dataset, type): %.2f"%(len(global_dict),(treduce-tend)))
#           print ("File open: %.2f\nData copy: %.2f\nFile close: %.2f\nTotal Cost: %.2f"%(topen-tcreated,tcopy-topen,tclose-tcopy,tclose-tstart))
if __name__=='__main__': 
    parallel_select()
