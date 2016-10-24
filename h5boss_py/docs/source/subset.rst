.. _subset:
Subset
========
The `subset` function can read the specified fiber object and copy into a single shared file. The input files are the BOSS data in HDF5 format. The user needs to specify the query as `plate mjd fiber`. The output file has same structure with the source files. 
 
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
 Source parse: 60.04
 Fiber copy: 1179.16
 Catalog copy: 382.07
 Total: 1653.67
 Done selection
 Total selection Cost 1653.67 seconds

For detailed performance test, please read our Techincal Report(To be released by Nov.1 2016).

High Performance Parallel Version:
------------------------
* :ref:`mpi4py <psubset>`
* :ref:`C-MPI <csubset>`
