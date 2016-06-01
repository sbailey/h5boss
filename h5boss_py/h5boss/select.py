import numpy as np
import h5py
import time
def select(infiles, outfile, plates, mjds, fibers):
    '''
    Select a set of (plates,mjds,fibers) from a set of input files
    
    Args:
        infiles : list of input filenames, or single filename
        outfile : output file to write the selection
        plates : list of plates
        mjds : list of plates
        fibers : list of fibers        
    '''
    #print (plates)
    plates = np.asarray(plates)
    mjds = np.asarray(mjds)
    fibers = np.asarray(fibers) 
    meta=['plugmap', 'zbest', 'zline',
			'photo/match', 'photo/matchflux', 'photo/matchpos']
    if not isinstance(infiles, (list, tuple)):
        infiles = [infiles,]
    hx = h5py.File(outfile,'w')
    tstart=time.time() 
    select_files=list() 
    print("plates/mjds/fiber found in: ") 
    for infile in infiles:
        try: 
         fx = h5py.File(infile, mode='r')
	except Exception, e:
         print ("File open error: ",infile)
         continue
        for plate in fx.keys():
            for mjd in fx[plate].keys():
                ii = (plates == plate) & (mjds == mjd)
		xfibers = fibers[ii]
		parent_id='{}/{}'.format(plate, mjd)
		if np.any(ii):
		   print (infile)
                   select_files.append(infile)
		   if parent_id not in hx:
                    hx.create_group(parent_id)
		   
                   for fiber in xfibers:
                       id = '{}/{}/{}'.format(plate, mjd, fiber)
		       if id not in hx:
                        fx.copy(id, hx[parent_id])                
                   for name in meta:
                       id = '{}/{}/{}'.format(plate, mjd, name)
                       catalog = fx[id]
                       yfib=xfibers.astype(np.int32)
                       jj = np.in1d(catalog['FIBERID'], yfib)
		       if id not in hx:
	                hx[id] = fx[id][jj].copy()
                #else: 
		#   print ("pmf not found in input file",infile) 
        fx.close()           
    hx.close()
    print("Selected %d files"%len(select_files))
    if(len(select_files)>0):
     selected_f="selected_files_"+str(len(select_files))+".out"
     print("Saved selected file path in %s"%str(selected_f))
     with open(selected_f,"wb") as f:
      f.writelines(["%s\n" % item  for item in select_files])
    tend=time.time()-tstart
    print ('Selection time: %.2f seconds'%tend)
