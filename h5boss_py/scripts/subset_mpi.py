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
from h5boss.selectmpi import add_dic
from h5boss.selectmpi import add_numpy
from h5boss.selectmpi import create_template
from h5boss.selectmpi import overwrite_template
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
        print ("rank:%d,file:%d"%(rank,len(range_files)))

        fiber_dict={}
        for i in range(0,len(range_files)):
            fiber_item = get_fiberlink(range_files[i],plates,mjds,fibers)
            if len(fiber_item)>0:
             inter_keys=fiber_dict.viewkeys() & fiber_item.viewkeys()
             if len(inter_keys)==0: 
                fiber_dict.update(fiber_item)
             else: 
                fiber_union(fiber_dict,fiber_item,inter_keys)
        tend=MPI.Wtime()
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
         print ("Allreduce %d fiber meta:kv(dataset, type): %.2f"%(len(global_fiber),(treduce-tend)))
        #sys.exit()  
        #Create the template using 1 process       
        if rank==0 and (template==1 or template==2):
           try:
            ##can not parallel create metadata is really painful. 
            create_template(outfile,global_fiber,'fiber',rank)
            catalog_number=count_unique(global_fiber) #(plates/mjd, num_fibers)
            print ('number of unique fibers:%d '%len(catalog_number))           
            #for fk,vk in catalog_number.items():
            #   print ("%s:%d"%(fk,vk))
            sample_file=range_files[0] # get the catalog metadata
            catalog_types=get_catalogtypes(sample_file) # dict: meta, (type, shape)
            global_catalog=(catalog_number,catalog_types)
            create_template(outfile,global_catalog,'catalog',rank)
           except Exception as e:
            traceback.print_exc()
        tcreated=MPI.Wtime()
        #if rank==0:
        #TODO: rewrite this to get the catalog and fiber in one shot
        copy_global_catalog=global_fiber
        revised_dict=locate_fiber_in_catalog(copy_global_catalog)
         #now revised_dict has: p/m, fiber_id, infile, global_offset
        copy_revised_dict=revised_dict.items()
        total_unique_fiber=len(copy_revised_dict)
        #distribute the workload evenly to each process
        step=int(total_unique_fiber / nproc)+1
        rank_start =int( rank * step)
        rank_end = int(rank_start + step)
        if(rank==nproc-1):
         rank_end=total_unique_fiber # adjust the last rank's range
         if rank_start>total_unique_fiber:
            rank_start=total_unique_fiber
        catalog_dict=copy_revised_dict[rank_start:rank_end]
        twritecsv_start=MPI.Wtime()
        if rank==0 and (template==1 or template==2):
         print ("Template creation time: %.2f"%(tcreated-treduce))
         with open(fiberout, 'a') as f:
           f.writelines('{}:{}\n'.format(k,v[2]) for k, v in global_fiber.items())
           f.write('\n')
         with open(catalogout, 'a') as f:
           for k,v in revised_dict.items():
            for iv in v:
             f.writelines('{}:{}:{}:{}\n'.format(k,iv[0],iv[1],iv[2]))
             #f.write('\n')
        twritecsv_end=MPI.Wtime()
        if rank==0:
         print ("count unique fiber and global offset time:%.2f"%(twritecsv_start-tcreated))
         print ("write fiber/catalog csv time: %.2f"%(twritecsv_end-twritecsv_start))
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
           #print ("rank:%d, start time:%s"%(rank, datetime.datetime.time(datetime.datetime.now())))
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
