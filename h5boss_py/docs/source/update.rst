.. _update:
Update
========

Usage:
------
.. highlight:: c 

update -h

usage::
 
  update [-h] base input pmf

positional arguments::

  base        Pre-subseted HDF5 file

  input       HDF5 input files list

  pmf         Plate/mjd/fiber list

optional arguments::

  -h, --help  show this help message and exit

Example:
--------
.. highlight:: c

prepare input::

 >cat input_sample.txt

  /global/cscratch1/sd/jialin/h5boss/3665-55247.hdf5

  ...

 >cat pmf_ssample.txt

  plates mjds fibers

  3665 55247 65

  3665 55247 390

  ...

download: :download:`input <_static/input_sample.txt>`, :download:`pmf <_static/pmf_ssample.txt>`, :download:`base.h5 <_static/base.h5>`

Execute command::

 >update base.h5 input_sample.txt pmf_sample.txt

Output::

 Query: Plates/Mjds/Fibers: 10
 Input: 2393 hdf5 files
 Output: base.h5 
 Running Updating:
 Query time: 0.00 seconds
 plates/mjds/fibers to be added: 10
 Running selection:
 -Source file open: 8.36
 -Fiber query time: 0.00
 -Fiber copy time: 0.25
 -Catalog copy time: 1.05
 -Group create time: 0.00
 -File close time: 0.04
 Selection Time: 12.74 seconds
 plates/mjds/fibers to be removed: 7
 Running removing:
 Removed 7 plates/mjds/fibers,Skipped 0
 Remvoing Time: 0.02 seconds
 Running repacking:
 Repacking Time: 2.75 seconds
 Updating complete: 16.58 seconds
