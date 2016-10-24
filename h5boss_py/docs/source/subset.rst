.. _subset:
Subset
========
The `subset` function can read the specified fiber object and copy into a single shared file. The input files are the HDF5 BOSS data. The user needs to specify the query as `plate mjd fiber`. The output file has same structure with the source files. 
 
Usage:
------
.. highlight:: c 


usage:: 

 subset [-h] input output pmf

positional arguments::

  input       HDF5 input list

  output      HDF5 output

  pmf         Plate/mjd/fiber list in csv

optional arguments::

  -h, --help  show this help message and exit

Example:
--------
.. highlight:: c

prepare input::

 >cat input_sample.txt

 /global/cscratch1/sd/jialin/h5boss/3665-55247.hdf5

 ...

 >cat pmf_sample.txt

 plates mjds fibers

 3665 55247 65

 3665 55247 390

 ...

download: :download:`input_sample.txt <_static/input_sample.txt>`, :download:`pmf_sample.txt <_static/pmf_sample.txt>`

Execute command::

 >subset input_sample.txt output.h5 pmf_sample.txt

Output::

 Output:  output.h5
 Running selection...
 Source: 60.04
 Fiber: 1179.16
 Catalog: 382.07
 column: 173.61
 entries: 125.84
 row: 79.86
 Total: 1653.67
 Done selection
 Total selection Cost 1653.67

For detailed performance test, please read our Techincal Report(To be released by Nov.1 2016).

High Performance Parallel Version:
------------------------
* :ref:`mpi4py <psubset>`
* :ref:`C-MPI <csubset>`
