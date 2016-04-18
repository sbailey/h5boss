import numpy as np
import h5py
import time
def pmj(infile, plates, mjds, fibers):
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
			 a=[int(pid),int(mid),int(fid)]
		         if a in pmj.tolist():
			    in_pmj.append(a)
			 else:
			    notin_pmj.append(a)	
			
    #notin_pmj contains pmj that is in in pre-existing subset but not in new list
    in_pmj=np.asarray(in_pmj)
    notin_pmj=np.asarray(notin_pmj) 
    #print in_pmj
    #print pmj
    in_pmj1d=np.core.records.fromarrays(in_pmj.transpose(),names='col1, col2, col3',formats='i8,i8,i8')    
    pmj1d=np.core.records.fromarrays(pmj.transpose(),names='col1, col2, col3',formats='i8,i8,i8')
    missing_pmj=np.setdiff1d(pmj1d,in_pmj1d)
    missing_pmj=missing_pmj.reshape(len(missing_pmj),1)
    tend=time.time()-tstart
    print "in subset, but new in pmj:\n"
    print notin_pmj
    print "\n"
    print "not in subset, but in pmj:\n"
    print missing_pmj
    print ('time', tend)
    return (missing_pmj, notin_pmj)
