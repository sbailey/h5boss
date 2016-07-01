import numpy as np
import h5py
import time
import traceback 
from multiprocessing import Pool
from mpi4py import MPI

plates=[]
mjds=[]
fibers=[]
meta=[]
hx=None
select_files=list()
outfile=""
def subselect(infile):
#	tstart=time.time()
        global select_files 
        global outfile,hx
        print (hx)
#	dwtime=0.0
#	dmwtime=0.0
#	print("plates/mjds/fiber found in: ") 
	#try: 
	#  hx=h5py.File(outfile,mode='w')
 	#except Exception,e:
	#  print("hx open error at time %.2f"%(time.time()))
        try: 
         fx = h5py.File(infile, mode='r')
        except Exception as e:
         print ("File open error: %s "%infile)
        finally: 
          pass
	#print (fx.keys())
        #print (plates)
        fiberlink=list()# for caching file handle, plates/mjd/fiber
        catalink=list()#for caching file hanlde, plates/mjd/cata, fiberid

        for plate in fx.keys():
            for mjd in fx[plate].keys():
                ii = (plates == plate) & (mjds == mjd)
                xfibers = fibers[ii]
                parent_id='{}/{}'.format(plate, mjd)
                if np.any(ii):
		   #print ("now reading file %s"%infile)
                  select_files.append(infile)
		   #print ("now the length of selected files is %d"%len(select_files))
		   #if parent_id not in hx:
		   # hx.create_group(parent_id)
	           # print ("group created at %.2f"%(time.time()),parent_id)
#		   dataw_start=time.time() 
                  for fiber in xfibers:
                       id = '{}/{}/{}'.format(plate, mjd, fiber)
                       if id not in hx:
                        try:
#			 fx.copy(id, hx[parent_id])
			 #instead of copying object here, try to cache the metadata info
                         temp_fiber=(fx,id)
                         if temp_fiber not in fiberlink:
                           fiberlink.append(temp_fiber)
			 #print("data object copied at %.2f"%(time.time()),id)
                        except Exception as e:
                         print("fiber %s not found"%id)
                         pass                
#		   dataw_end=time.time()
#		   dwtime+=dataw_end-dataw_start
	  
                  for name in meta:
                       id = '{}/{}/{}'.format(plate, mjd, name)
                       try:
                        catalog = fx[id]
                        yfib=xfibers.astype(np.int32)
                        jj = np.in1d(catalog['FIBERID'], yfib)
                        if id not in hx:
			 #hx[id] = fx[id][jj].copy()
			 #instead of copying the object, saving the info
			 # id(plates/mjds/plugmap), jj(catalog['fiberid']), and fx
                         temp_meta=(fx,id,jj)
                         if temp_meta not in metalink:
                           metalink.append(temp_meta)
		 #        print ("catalog object copied ",id)
                       except Exception as e:
                        print("catalog %s not found"%id)
                        pass
	#	   datamw_end=time.time()
#		   dmwtime+=datamw_end-dataw_end
		#else: 
		#   print ("pmf not found in input file",infile) 
        fx.close()          
        try:
         hx.close()
         #print ("hx is closed at %.2f"%(time.time())) 
        except Exception as e:
         print ("child closing file error")
	#tend=time.time()-tstart
	#print ('Total selection time: %.2f seconds'%tend)
	#print ('Data read/write time: %.2f seconds'%dwtime)
	#print ('Catalog read/write timne: %.2f seconds'%dmwtime)
	#print ('Metadata operation time: %.2f seconds'%(tend-dwtime-dmwtime))

        return (fiberlink,metalink)
def select(infiles, outfiles, platess, mjdss, fiberss, nproc=None, mpiop=None):
    '''
    Select a set of (plates,mjds,fibers) from a set of input files
    
    Args:
        infiles : list of input filenames, or single filename
        outfile : output file to write the selection
        plates : list of plates
        mjds : list of plates
        fibers : list of fibers        
    '''
    global plates,mjds,fibers,meta,hx,select_files
    plates = np.asarray(platess)
    mjds = np.asarray(mjdss)
    fibers = np.asarray(fiberss)
    meta=['plugmap', 'zbest', 'zline',
                        'photo/match', 'photo/matchflux', 'photo/matchpos']
    if not isinstance(infiles, (list, tuple)):
        infiles = [infiles,]
    global outfile,hx
    outfile=outfiles
    try:
     hx = h5py.File(outfile,'w',driver='core')
    except Exception as e:
     print ("create final file error:%s"%outfile)
    tstart=time.time()
    print ("total hdf5 files %d"%len(infiles))
    ######################  MPI ########################
    if mpiop != None and mpiop =="yes": 
     print ("Using mpi4py")
     comm =MPI.COMM_WORLD
     nproc = comm.Get_size()
     rank = comm.Get_rank()
     if (rank==0):
     	print ("starting mpi routine with %d processes"%nproc)  
     #each rank gets a subset of the filelist
     total_files=len(infiles)
     #distribute the workload evenly to each process
     step=total_files / nproc
     rank_start = rank * step
     rank_end = rank_start+step
     if(rank==nproc-1):
        rank_end=total_files
     range_files=infiles[rank_start:rank_end]
     #each rank starts the subselect procedure
     fiberlink=[]
     metalink=[]
     for i in range(0,len(range_files)):
      (fiber_item,meta_item)=subselect(range_files[i])
      fiberlink.append(fiber_item)
      metalink.append(meta_item)
    ##################### MultiProcessing ##############
    elif nproc != None and nproc>1:
     print ("Using %d processes with multiprocessing python on single node"%nproc)
     p=Pool(nproc)
     p.map(subselect, infiles)
     #p.join
    ##################### Serial Version ##############    
    else:
     print ("Using 1 process")
     map(subselect,infiles)  
    print("Selected %d files"%len(select_files))
    if(len(select_files)>0):
     selected_f="selected_files_"+str(len(select_files))+".out"
     print("Selected file info saved in %s"%str(selected_f))
     with open(selected_f,"wb") as f:
      f.writelines(["%s\n" % item  for item in select_files])
    print ('Total Cost: %.2f'%(time.time()-tstart))
