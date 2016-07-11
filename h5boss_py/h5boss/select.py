import numpy as np
import h5py
import time
import traceback
#def select(infiles, outfile, plates, mjds, fibers,nproc):
def select(infiles, outfile, plates, mjds,fibers):
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
    meta=['plugmap', 'zbest', 'zline', 'photo/match', 'photo/matchflux', 'photo/matchpos']
    if not isinstance(infiles, (list, tuple)):
        infiles = [infiles,]
    #hx = h5py.File(outfile,'w')
    tstart=time.time() 
    select_files=list() 
    dwtime=0.0
    #print("plates/mjds/fiber found in: ") 
    for infile in infiles:
        try: 
         fx = h5py.File(infile, mode='r')
        except Exception as e:
         print ("File open error: ",infile)
         continue
        for plate in fx.keys():
            for mjd in fx[plate].keys():
                ii = (plates == plate) & (mjds == mjd)
                xfibers = fibers[ii]
                parent_id='{}/{}'.format(plate, mjd)
                if np.any(ii):
                   #print (infile)
                   select_files.append(infile)
                   try:
                    hx = h5py.File(outfile,'w')
                   except:
                    pass
                   if parent_id not in hx:
                    hx.create_group(parent_id)
                   dataw_start=time.time() 
                   for fiber in xfibers:
                       id = '{}/{}/{}'.format(plate, mjd, fiber)
                       if id not in hx:
                        try:
			 #this is the object copy
                         fx.copy(id, hx[parent_id])
                        except Exception as e:
                         print("fiber %s not found"%id)
                         pass                
                   for name in meta:
                       id = '{}/{}/{}'.format(plate, mjd, name)
                       try:
                        catalog = fx[id]
                        yfib=xfibers.astype(np.int32)
                        jj = np.in1d(catalog['FIBERID'], yfib)
                        if id not in hx:
                         dset=hx.create_dataset(id,maxshape=(None,),dtype=fx[id][jj].dtype,data=fx[id][jj])
			 #this is the dataset slice copy,i.e., only copy the row that has the queried fiberid
                         #hx[id] = fx[id][jj].copy()
                        else:
                         if fx[id][jj]['FIBERID'] not in hx[id]['FIBERID']:
                          dset=hx[id]
                          dset.resize(len(dset)+1)
                          dset[len(dset)-1]=fx[id][jj]
                          dset.close()
			#exist_id=hx[id] # catalog table is existed, need to update
                       except Exception as e:
                        print("catalog %s add error"%id)
                        traceback.print_exc()
                        pass
                   dataw_end=time.time()
                   dwtime+=dataw_end-dataw_start
                #else: 
		#   print ("pmf not found in input file",infile) 
        fx.close()           
    try:
     hx.close()
    except:
     pass
    #print("Selected %d files"%len(select_files))
    if(len(select_files)>0):
     selected_f="selected_files_"+str(len(select_files))+".out"
     #print("Selected file info saved in %s"%str(selected_f))
     with open(selected_f,"wt") as f:
      f.writelines(["%s\n" % item  for item in select_files])
    tend=time.time()-tstart
    #print ('Selection time: %.2f seconds'%tend)
    #print ('Data write time: %.2f seconds'%dwtime)
    #print ('Metadata operation time: %.2f seconds'%(tend-dwtime))
