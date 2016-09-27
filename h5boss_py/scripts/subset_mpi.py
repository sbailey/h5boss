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
from h5boss.pmf import locate_fiber_in_catalog
from h5boss.pmf import dedup
from h5boss.selectmpi import add_dic
from h5boss.selectmpi import add_numpy
from h5boss.selectmpi import create_template
from h5boss.selectmpi import overwrite_template
from h5boss.h5map import datamap
from time import gmtime, strftime
import datetime
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
    parser.add_argument("--template", help="Create template only,yes/no/all")
    parser.add_argument("--mpi", help="using mpi yes/no")
    parser.add_argument("--fiber", help="specify fiber csv output")
    parser.add_argument("--catalog", help="specify catalog csv output")
    opts=parser.parse_args()

    infiles = opts.input
    outfile = opts.output
    pmflist = opts.pmf
    fiberout = "fibercsv"
    catalogout = "catalogcsv"
    if opts.fiber:
     fiberout = opts.fiber
    if opts.catalog:
     catalogout = opts.catalog
    catalog_meta=['plugmap', 'zbest', 'zline',
                        'match', 'matchflux', 'matchpos']
    meta=['plugmap', 'zbest', 'zline',
                        'photo/match', 'photo/matchflux', 'photo/matchpos']
    if opts.template is None or opts.template=="no":
       template=0
    elif opts.template and opts.template=="yes":
       template=1
    elif opts.template and opts.template=="all":
       template=2
    if opts.mpi is None or opts.mpi=="no": 
        #starts seirial processing
        print ("Try the subset.py or subset command")
        sys.exit()
    elif opts.mpi and opts.mpi=="yes":
        comm =MPI.COMM_WORLD
        nproc = comm.Get_size()
        rank = comm.Get_rank()
        tstartcsv=MPI.Wtime()
        (plates,mjds,fibers,hdfsource) = parse_csv(infiles, outfile, pmflist,rank)
        tstart=MPI.Wtime()
        if rank==0: 
           print ("Number of processes %d"%nproc)
           print ("parse csv time: %.2f"%(tstart-tstartcsv))
        total_files=len(hdfsource)
        #distribute the workload evenly to each process
        step=int(total_files / nproc)
        rank_start =int( rank * step)
        rank_end = int(rank_start + step)
        if(rank==nproc-1):
            rank_end=total_files # adjust the last rank's range
            if rank_start>total_files:
             rank_start=total_files
        range_files=hdfsource[rank_start:rank_end]
        #print ("rank:%d,file:%d"%(rank,len(range_files)))
        if rank==0:
          sample_file=range_files[0]
        fiber_dict={}
        for i in range(0,len(range_files)):
            fiber_item = get_fiberlink(range_files[i],plates,mjds,fibers)
            #print ("p:%dm:%df:%d"%(len(plates),len(mjds),len(fibers)))
            #print("len(fiber_item):%d"%(len(fiber_item)))
            if len(fiber_item)>0:
             inter_keys=fiber_dict.viewkeys() & fiber_item.viewkeys()
             if len(inter_keys)==0: 
                fiber_dict.update(fiber_item)
             else: 
                fiber_dict=fiber_union(fiber_dict,fiber_item,inter_keys)
        tend=MPI.Wtime()
        #print ("rank:%d,fiber_dict:%d"%(rank,len(fiber_dict)))
        if rank==0: 
         print ("Get metadata of fiber ojbect time: %.2f"%(tend-tstart))
        #rank0 create all, then close an reopen.-Quincey Koziol 
        counterop = MPI.Op.Create(add_dic, commute=True) #define reduce operation
        global_fiber={}#(key, value)->(plates/mjd/fiber/../dataset, (type,shape,filename), unordered
        fiber_item_length=len(fiber_dict)
        fiber_dict_tmp=fiber_dict
        global_fiber= comm.allreduce(fiber_dict_tmp, op=counterop)       
        treduce=MPI.Wtime()
        #print ("rank: ",rank,fiber_dict_tmp_numpy)
        if rank==0:
         print ("Allreduce dics: %.2f"%((treduce-tend)))
         print ("len(global_fiber):%d"%(len(global_fiber)))
         print (global_fiber) # expect: key(plate/mjd), value(filename, fiberlist, fiberoffsetlist)
         #for igf in global_fiber:
         #  print("key:%s,values:%s"%(igf,global_fiber[igf]))
        # remove duplication of fiberlist and fiberoffsetlist in global_fiber
        if rank==0:
         import cPickle
         dup_gf=cPickle.dumps(global_fiber) 
         dup_size=sys.getsizeof(dup_gf)
         dup_len=len(global_fiber)
         global_fiber=dedup(global_fiber)
         dedup_gf=cPickle.dumps(global_fiber)
         dedup_size=sys.getsizeof(dedup_gf)
         dedup_len=len(global_fiber)
         print("Before dedup: %d bytes. After dedup:%d bytes"%(dup_size,dedup_size))
         print("Before dedup: %d pm. After dedup:%d pm"%(dup_len,dedup_len))
        # get datamap,i.e., type and shape of each dataset in coadds and exposures. 
        #sys.exit()
        if rank==0:
         dmap1=datamap(sample_file)
         print ("Datamap is:")
         for imap in dmap1:
           for ikey in imap:
             print ("dataset:%s type:%s shape:%s"%(ikey,imap[ikey][0],imap[ikey][1])) 
        #sys.exit()  
        #Create the template using 1 process       
        if rank==0 and (template==1 or template==2):
           try:
            create_template(outfile,global_fiber,dmap1,'fiber',rank)
           except Exception as e:
            traceback.print_exc()
        tcreated=MPI.Wtime()
        twritecsv_start=MPI.Wtime()
        if rank==0 and (template==1 or template==2):
         print ("Template creation time: %.2f"%(tcreated-treduce))
         twritecsv_end=MPI.Wtime()
        #if rank==0:
############# OVERWRITE THE TEMPLATE WITH ACTUAL DATA ############
        if template ==0 or template==2: 
         try: 
          hx = h5py.File(outfile,'a',driver='mpio', comm=MPI.COMM_WORLD) ## collectively open file 
          hx.atomic=False 
         except Exception as e:
          traceback.print_exc()        
        topen=MPI.Wtime()
        tclose=topen        
        fiber_copyte=topen
        fiber_copyts=topen
        catalog_copyts=topen
        catalog_copyte=topen
        if template==0 or template==2:
           fiber_copyts=MPI.Wtime()
           print ("rank:%d, fiber_dict length:%d"%(rank,fiber_item_length))
           fiber_copy_start=time.time()
           overwrite_template(hx,fiber_dict,'fiber')
           fiber_copy_end=time.time()
           print("rank:%d,fibercost:%.2f"%(rank,fiber_copy_end-fiber_copy_start))
           fiber_copyte=MPI.Wtime()
           #for each fiber, find the catalog, then copy it
           catalog_copyts=MPI.Wtime()
           #overwrite_template(hx,catalog_dict,'catalog')
           catalog_copyte=MPI.Wtime()
           hx.close()
           tclose=MPI.Wtime()
           #print("rank:%d,fiber cost:%.2f"%(rank,fiber_copyte-fiber_copyts))
        if rank==0:
           print ("File open: %.2f\nFiber copy: %.2f\nCatalog copy: %.2f\nFile close: %.2f\nTotal Cost: %.2f"%(topen-tcreated,fiber_copyte-fiber_copyts,catalog_copyte-catalog_copyts,tclose-catalog_copyte,tclose-tstart))
if __name__=='__main__': 
    parallel_select()
