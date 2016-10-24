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

 Will repack the file for better storage layout afterwards.
 PMF: Plates/Mjds/Fibers: 10
 Input: 2393 files
 Output: base.h5 
 Running selection:
 Query time: 0.00 seconds
 plates/mjds/fibers to be added: 10
 -Source file open: 2.06
 -Fiber copy: 0.21
 -Catalog copy: 0.85
 -Group create: 0.00
 -File close: 0.04
 Total cost in fiber/catalog selection: 7.12 seconds
 plates/mjds/fibers to be removed: 7
 Removed 7 pmf,Skipped 0
 Remvoing time:0.02
 Repack time:2.39
 Done selection: 10.46 seconds totally

