#!/usr/bin/env python
"""
Create an HDF5 file from BOSS data

TODO:
  - include comments in meta/attrs
  - platelist quantities
"""
from __future__ import division, print_function
#from __future__ import absolute_import
from h5boss.selectmpi import select
import sys,os
import time
import optparse
import csv
import traceback
import pandas as pd
import numpy as np
import optparse
import argparse
from mpi4py import MPI
parser = argparse.ArgumentParser(prog='subset')
parser.add_argument("input",  help="HDF5 input list")
parser.add_argument("output", help="HDF5 output")
parser.add_argument("pmf",    help="Plate/mjd/fiber list in csv")
parser.add_argument("--nproc", help="number of processes",type=int)
parser.add_argument("--mpi", help="using mpi yes/no")
opts=parser.parse_args()


#parser = optparse.OptionParser(usage = "%prog [options]")
#parser.add_option("-i", "--input", type=str,  help="input file list")
#parser.add_option("-o", "--output", type=str,  help="output hdf5")
#parser.add_option("-x", "--xls", type=str,help="pmf excel")
#parser.add_option("-l", "--pmf",type=str,help="pmf csv")
#opts, args = parser.parse_args()

#xlsfile = opts.xls
pmflist = opts.pmf
infiles = opts.input
outfile = opts.output
nproc=1
if opts.nproc:
 nproc = opts.nproc
tstart=time.time()
#import pandas as pd
#try: 
# df = pd.ExcelFile(xlsfile).parse('Sheet1')
# plates = map(str,df['plates'].values.tolist())
# mjds = map(str,df['mjds'].values.tolist())
# fibers = map(str,df['fibers'].values.tolist())

#except Exception, e:
# print("excel read error or not exist:%s"%e,xlsfile)
 #traceback.print_exc()
plates=[]
mjds=[]
fibers=[]
try:
 df = pd.read_csv(pmflist,delimiter=' ',names=["plates","mjds","fibers"],index_col=None,dtype=str)
 df = df.sort(['plates'],ascending=[1])
 #plates = map(str,df['plates'].values.tolist())
 plates = list(map(str,df['plates'].values))
 plates_array = np.asarray(plates)
 plates_uni_array = np.unique(plates_array)
 print ("number of unique plates is %d"%plates_uni_array.size)
# print (plates)
 #mjds = map(str,df['mjds'].values.tolist())
 #fibers = map(str,df['fibers'].values.tolist())
 mjds = list(map(str,df['mjds'].values))
 fibers = list(map(str,df['fibers'].values))
except Exception as e:
 print("pmf csv read error or not exist:%s"%e,pmflist)
 print("e.g., 1st row of csv should be 'plates mjds fibers'")
infile=[]
try:
 with open(infiles,'rt') as f:
  reader = csv.reader(f)
  infile = list(reader)
  infile = [x for sublist in infile for x in sublist]
except Exception as e:
 print ("input filelist csv read error or not exist: %s"%e,infiles)
 #traceback.print_exc()

#infile = [x for sublist in infile for x in sublist]
#print ("Plates: ",plates)
#print ("MJDs: ",mjds)
#print ("Fibers: ", fibers)
#print ("plates:",plates)
#print ("infile:",infile)
if(len(plates)==0 or len(infile)==0):
  print("pmf or input is empty")
  sys.exit(0)

print ("Input: %d files:"%len(infile),infile[0],"...",infile[-1])
print ("Output: ", outfile)
print ("Running selection...")
comm =MPI.COMM_WORLD
mpiop= None
if opts.mpi and opts.mpi=="yes":
 mpiop=comm
try:
 select(infile, outfile, plates, mjds, fibers,nproc,mpiop)
except Exception as e:
 print ("Error in select:")
 traceback.print_exc()
print ("Done selection")
