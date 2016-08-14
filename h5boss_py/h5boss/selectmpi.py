import numpy as np
import h5py
import time,os
import traceback 
from h5boss.pmf import pmf 
from h5boss.select import select


## Global variables:
## Data structure of fiberdatalink: {key, value_pair()} --->  {path_dataset, (datatype,datashape,filename)}
## For example fiberdatalink['3665/52273/360/coadd']= (V32, $SCRATCH/h5boss/3665-52273.h5)
## Aug 3 2016
## Jialin Liu, jalnliu@lbl.gov
# create_slavefile is used in ../script/subset_mpi-sf.py, which creates multiple sub files 
def create_slavefile(infile,plates,mjds,fibers,masterfile,rank,id):
    master_dir=os.path.dirname(os.path.realpath(masterfile))+'/'+os.path.basename(masterfile).split('.')[0]
     
    slavefile=master_dir+'/'+str(rank)+'_'+str(id)+'.h5'
    try:
      select(infile, slavefile, plates, mjds, fibers)
    except Exception as e:
      print ("Error in slave file:%s")
      traceback.print_exc()
      pass 
def _adddic(dict1,dict2,datatype):
    for item in dict2:
      if item not in dict1:
        dict1[item] = dict2[item]
    return dict1

def create_template(outfile,global_dict):
 try:
     hx = h5py.File(outfile,'a')
 except Exception as e:
     print ("Output file creat error:%s"%outfile)
     traceback.print_exc()
 try:#Set the allocate time as early. --Quincey Koziol 
  for key,value in global_dict.items():
    if key.split('/')[-1] not in catalog_meta:
     _fiber_template(hx,key,value)
    else:
     _catalog_template(hx,key,value)
 except Exception as e:
   traceback.print_exc()
   pass
 try:
  hx.flush()
  hx.close()
 except Exception as e:
  print("hx close error in rank0")
  traceback.print_exc()
  pass
def _fiber_template(hx,key,value):
   space=h5py.h5s.create_simple(value[1])
   plist=h5py.h5p.create(h5py.h5p.DATASET_CREATE)
   plist.set_alloc_time(h5py.h5d.ALLOC_TIME_EARLY)
   tid=h5py.h5t.py_create(value[0], False)
   try:#create intermediate groups
      hx.create_group(os.path.dirname(key))
   except Exception as e:
      pass #groups existed, so pass it
   try:
    h5py.h5d.create(hx.id,key,tid,space,plist)#create dataset with property list:early allocate
   except Exception as e:
    print("dataset create error: %s"%key)
    traceback.print_exc()
    pass
def _catalog_template(hx,key,value):
   space=h5py.h5s.create_simple(value[1])
   plist=h5py.h5p.create(h5py.h5p.DATASET_CREATE)
   plist.set_alloc_time(h5py.h5d.ALLOC_TIME_EARLY)
   tid=h5py.h5t.py_create(value[0], False)
   try:#create intermediate groups
      hx.create_group(os.path.dirname(key))
   except Exception as e:
      pass #groups existed, so pass it
   try:
    h5py.h5d.create(hx.id,key,tid,space,plist)#create dataset with property list:early allocate
   except Exception as e:
    print("dataset create error: %s"%key)
    traceback.print_exc()
    pass

def copy_all(hx, fiber_dict):
 #Read/Write all dataset into final file, 
 #each rank handles one fiber_dict, which contains multiple fiber_item
 try:
  for key, value in fiber_dict.items():
    if key.split('/')[-1] not in catalog_meta:
     _copy_fiber(hx,key,value)
     if key.split('/')[-1]=='coadd':
      fiber_id=key.split('/')[-2]
      _copy_catalog(hx,key,value,fiber_id)
 except Exception as e:
  print ("Data read/write error key:%s file:%s"%(key,value[2]))
  traceback.print_exc()
  pass

def _copy_fiber(hx,key,value):
 try:
  subfx=h5py.File(value[2],'r')
  subdx=subfx[key].value
  subfx.close()
 except Exception as e:
  traceback.print_exc()
  print ("read subfile %s error"%value[2])
  pass
 try:
  dx=hx[str(key)]
  dx[:]=subdx   #overwrite the existing template data
 except Exception as e:
  traceback.print_exc()
  print ("overwrite error")
  pass
def _copy_catalog(hx,key,value,fiber_id):
   try:
    #print ("open catalog now")
    fx=h5py.File(value[2],'r')
    #fiber=key.split('/')[-2]
    plate=key.split('/')[0]
    mjd=key.split('/')[1]
    for name in meta:
     id = '{}/{}/{}'.format(plate,mjd,name)
     hx[id][int(fiber_id)-1]=fx[id][int(fiber_id)-1]
     print ("catalog:%s row id:%d"%(id,int(fiber_id)-1))
     #print ("src catalog:",fx[id][int(fiber)-1])
   except Exception as e:
    traceback.print_exc()
    print ("catacopy:%s error:%d"%(key,int(fiber_id)-1))  
