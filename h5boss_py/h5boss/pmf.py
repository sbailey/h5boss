import numpy as np
import h5py
import time
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
    plates = np.asarray(plates).reshape(len(plates),1)
    mjds = np.asarray(mjds).reshape(len(mjds),1)
    fibers = np.asarray(fibers).reshape(len(fibers),1)
    pm=np.concatenate((plates,mjds),axis=1)
    pmj=np.concatenate((pm,fibers),axis=1)
    inx=h5py.File(infile,'r')
    in_pmj=[]
    notin_pmj=[]
    for pid in inx.keys():
	for mid in inx[pid].keys():
		for fid in inx[pid+'/'+mid].keys():
			if fid.isdigit():
			 a=[str(pid),str(mid),str(fid)]
			 print a
		         if a in pmj.tolist():
			    print ('in')
			    in_pmj.append(a)
			 else:
			    print ('not in')
			    notin_pmj.append(a)	
			
    #notin_pmj contains pmj that is in in pre-existing subset but not in new list
    in_pmj=np.asarray(in_pmj)
    notin_pmj=np.asarray(notin_pmj) 
    #print in_pmj
    #print pmj
    #print notin_pmj
    in_pmj1d=np.core.records.fromarrays(in_pmj.transpose(),names='col1, col2, col3',formats='a25,a25,a25')    
    pmj1d=np.core.records.fromarrays(pmj.transpose(),names='col1, col2, col3',formats='a25,a25,a25')
    missing_pmj=np.setdiff1d(pmj1d,in_pmj1d)
    missing_pmj=missing_pmj.reshape(len(missing_pmj),1)
    tend=time.time()-tstart
    print "in pre_subset, but not in pmf list:%d\n"%len(notin_pmj)
    print notin_pmj
    print "\n"
    print "not in pre_subset, but in pmf list:%d\n"%len(missing_pmj)
    print missing_pmj
    print ('time', tend)
    return (missing_pmj, notin_pmj)
