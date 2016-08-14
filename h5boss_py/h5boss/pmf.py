import numpy as np
import h5py
import time
import sys

fx=""
pid=""
inputfile=""
fiberdatalink={}
cataloglink={}
meta=['plugmap', 'zbest', 'zline',
                        'photo/match', 'photo/matchflux', 'photo/matchpos']

def pmf(infile, plates, mjds, fibers):
    '''
    check (plates,mjds,fibers) in the source hdf5 file
    return the matched/missed pmf

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

def parse_csv(input,output,pmflist,rank):
    '''
        Check the input/output and pmflist
        return plates, mjds, fibers as separate numpy arrays 
    Args:
        input:   HDF5 files list, i.e., source data
        output:  HDF5 file, to be created or updated
        pmflist: Plates/mjds/fibers numbers to be quried
    '''
    # check output file and its path
    if os.path.exists(output):
        if rank==0:
         print ("The output file %s is existed, your job is going to overwrite it or update it"%output)
    elif os.access(os.path.dirname(output),os.W_OK):
        if rank==0:
         print ("The output file %s is not existed, your job will create a new file"%output)
    else:
        if rank==0:
         print ("The output file's path does not exist, job exits now")
        sys.exit()

    # parse plates/mjds/fibers    
    plates=[]
    mjds=[]
    fibers=[]
    try:
        df = list_csv(pmflist)
        plates = df['plates']
        mjds = df['mjds']
        fibers = df['fibers']
    except Exception as e:
        print("pmflist csv read error or not exist:%s"%e,pmflist)
        traceback.print_exc()
        print("Note: 1st row of csv should start with 'plates mjds fibers'")
    if len(plates)==0:
        print ("No query is found, plate is empty")
        sys.exit()
    
    try:
        with open(input,'rt') as f:
         reader = csv.reader(f)
         hdfsource = list(reader)
        hdfsource = [x for sublist in hdfsource for x in sublist]
    except Exception as e:
        print ("HDF5 inputlist csv read error or not exist: %s"%e,input)

    if(len(hdfsource)==0):
        print("HDF5 source is empty")
        sys.exit(0)

    plates = np.asarray(plates)
    mjds = np.asarray(mjds)
    fibers = np.asarray(fibers)

    return (plates,mjds,fibers,hdfsource)


def list_csv(x):
    '''
       Return a array[list], where each list is a column
    Args:
        csv file
    '''
    columns = defaultdict(list) # each value in each column is appended to a list
    try:
     with open(x) as f:
      reader = csv.DictReader(f,delimiter=' ') # read rows into a dictionary format
      for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k
    except Exception as e:
     print ("read pmf csv error")
     traceback.print_exc()
     sys.exit()
    return columns

def _traverse_fibernode(name):
    '''
       para   : node name in a hdf5 group
       purpose: Find a dataset node, which should be an endpoint in its group hierarchy
       return : (key,value)->(path_to_dataset, (dataset type, shape, filename)) 
    '''
    global fx,pid,fiberdatalink,inputfile
    try:
     cur_node=name.encode('ascii','ignore')
     node=pid+'/'+cur_node
     node_t=str(type(fx[node]))
     if 'dataset' in node_t:
        node_t=fx[node].dtype
        node_sp=fx[node].shape
        fiberdatalink[node]=(node_t,node_sp,inputfile)
    except Exception as e:
     traceback.print_exc()
     pass

#node_type is used in ../script/subset_mpi.py, which is to create single shared file 
def get_fiberlink(infile,plates,mjds,fibers):
        '''
           para  : filename, plate, mjd, fiber
           return: (key, value)->(plates/mjd/fiber/../dataset, (type,shape,filename))
           python dict's updating can ensure that the key is unique, i.e., plate/mjd/fiber/../dataset is unique
        '''
        global pid,fiberdatalink, cataloglink, fx, inputfile
        inputfile=infile
        try:
         fx = h5py.File(infile, mode='r')
         for plate in fx.keys():
            for mjd in fx[plate].keys():
                ii = (plates == plate) & (mjds == mjd)
                spid= '{}/{}'.format(plate, mjd)
                xfibers = fibers[ii]
                if np.any(ii): # fiber is found
                  for fiber in xfibers:#for each fiber node, recursively visit its members and record the 
                      #fiberlink={id:infile}
                      pid = '{}/{}/{}'.format(plate, mjd, fiber)
                      fx[pid].visit(_traverse_fibernode)
                for im in meta:
                  mnode=spid+'/'+im
                  mnode_t=fx[mnode].dtype
                  mnode_sp=fx[mnode].shape
                  fiberdatalink[mnode]=(mnode_t,mnode_sp,infile)
         fx.close()
        except Exception as e:
         print (pid)
         traceback.print_exc()
         print (pid,infile)
         pass
        return (fiberdatalink)
