import numpy as np
import h5py
import time
import traceback 
from mpi4py import MPI

meta=['plugmap', 'zbest', 'zline',
                        'photo/match', 'photo/matchflux', 'photo/matchpos']
hx=None
select_files=list()
outfile=""
def select(infile,plates,mjds,fibers):
#	tstart=time.time()
        global select_files,meta 
        global outfile,hx
        #print (hx)
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
        metalink=list()#for caching file hanlde, plates/mjd/cata, fiberid

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
                       #if id not in hx:
                       try:
#			 fx.copy(id, hx[parent_id])
			 #instead of copying object here, try to cache the metadata info
                         temp_fiber=(fx,id)
                         if temp_fiber not in fiberlink:
			   print ("temp_fiber:",temp_fiber)
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
                        #if id not in hx:
			 #hx[id] = fx[id][jj].copy()
			 #instead of copying the object, saving the info
			 # id(plates/mjds/plugmap), jj(catalog['fiberid']), and fx
                        temp_meta=(fx,id,jj)
                        if temp_meta not in metalink:
			   print ("temp_meta:",temp_meta)
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
        #try:
        # hx.close()
         #print ("hx is closed at %.2f"%(time.time())) 
        #except Exception as e:
        # print ("child closing file error")
	#tend=time.time()-tstart
	#print ('Total selection time: %.2f seconds'%tend)
	#print ('Data read/write time: %.2f seconds'%dwtime)
	#print ('Catalog read/write timne: %.2f seconds'%dmwtime)
	#print ('Metadata operation time: %.2f seconds'%(tend-dwtime-dmwtime))

        return (fiberlink,metalink)
