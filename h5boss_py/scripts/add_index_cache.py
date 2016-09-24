import h5py
import os
from os import listdir
from os.path import isfile, join

mypath="/global/cscratch1/sd/jialin/h5boss_v2"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
class Index(object):
   def __init__(self,filename, dataset="plugmap"):
      self.filename=filename
      self.dataset=dataset
   def add(self):
      with h5py.File(self.filename,'a') as f:
         data=f[self.dataset]
         data_value=data.value
         # generate default index, 
         id0= range(1,1001)
         
         
   def drop(self):



