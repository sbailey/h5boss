import numpy as np
import h5py
import time
import sys

def pmf(infile, plates, mjds, fibers):
    '''
    check (plates,mjds,fibers) against the input file
    
    Args:
        infile : input file
        plates : list of plates
        mjds : list of plates
        fibers : list of fibers        
    '''
    tstart=time.time()
    if(len(plates)==0 or len(mjds)==0 or len(fibers)==0 or len(infile)==0):
      print('input is empty')
      sys.exit(0)
    plates = np.asarray(plates).reshape(len(plates),1)
    mjds = np.asarray(mjds).reshape(len(mjds),1)
    fibers = np.asarray(fibers).reshape(len(fibers),1)
    pm=np.concatenate((plates,mjds),axis=1)
    pmf=np.concatenate((pm,fibers),axis=1)
    inx=h5py.File(infile,'r')
    in_pmf=[]
    notin_pmf=[]
    for pid in inx.keys():
	for mid in inx[pid].keys():
		for fid in inx[pid+'/'+mid].keys():
			if fid.isdigit():
			 a=[str(pid),str(mid),str(fid)]
			 #print a
		         if a in pmf.tolist():
			    #print ('in')
			    in_pmf.append(a)
			 else:
			    #print ('not in')
			    notin_pmf.append(a)	
			
    #notin_pmf contains pmf that is in in pre-existing subset but not in new list
    in_pmf=np.asarray(in_pmf)
    notin_pmf=np.asarray(notin_pmf)
    tend=time.time()-tstart
 
    if(len(in_pmf)>0):
     in_pmf1d=np.core.records.fromarrays(in_pmf.transpose(),names='col1, col2, col3',formats='a25,a25,a25')    
     pmf1d=np.core.records.fromarrays(pmf.transpose(),names='col1, col2, col3',formats='a25,a25,a25')
     missing_pmf=np.setdiff1d(pmf1d,in_pmf1d)
     missing_pmf=missing_pmf.reshape(len(missing_pmf),1)
     print "Fibers found in pmf list, but not in the pre-existing file: %d"%len(missing_pmf)
    else: 
      missing_pmf=np.empty(0)
    if(len(notin_pmf)>0):
     notin_pmf=np.core.records.fromarrays(notin_pmf.transpose(),names='col1, col2, col3',formats='a25,a25,a25')
     print "Fibers found in the pre-existing file, but not in the pmf list: %d"%len(notin_pmf)
    else:
     notin_pmf=np.empty(0)
    print ('Metadata query time: %.2f seconds'%tend)
    return (missing_pmf, notin_pmf)
