.. _subset:
Subset
========
The `subset` function will find the specified plates/mjds/fibers from source files and copy into a single shared output. The source files are the BOSS data in HDF5 format. The user needs to specify the query as `plate mjd fiber`. The output file has a same structure with the source files. 
 
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

Prepare input::

 cat input_sample.txt

 /global/cscratch1/sd/jialin/h5boss/3665-55247.hdf5

 ...

 cat pmf_sample.txt

 plates mjds fibers

 4562 55570 622

 4479 55592 543

 7294 56739 242

 ...

Download: :download:`input_sample.txt <_static/input_sample.txt>`, :download:`pmf_sample.txt <_static/pmf_sample.txt>`

Execute command::

 subset input_sample.txt output.h5 pmf_sample.txt

Output::

 Output:  output.h5
 Running selection...
 -Source file open: 2.04
 -Fiber query time: 0.00
 -Fiber copy time: 11.35
 -Catalog copy time: 6.70
 -Group create time: 0.01
 -File close time: 0.04
 Selection Time: 22.34 seconds
 Done selection
 Total selection Cost 22.34


For detailed performance evaluation, please read our Techincal Report(To be released by Nov.1 2016).

High Performance Parallel Version:
------------------------
* :ref:`mpi4py <psubset>`
* :ref:`C-MPI <csubset>`
