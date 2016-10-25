.. _update:
Update
========
Given a plate/mjd/fiber query list. This `update` command will update the base hdf5 accordingly. Basically, `update` will
  * Compare the existing plate/mjd/fibers in the base hdf5 file with this query, 
  * Search the new plate/mjd/fiber, which are not existed in the base hdf5 file, from the input hdf5 files
  * Add the founded plate/mjd/fiber into the base file
  * Remove the existing plate/mjd/fiber from the base file, which are not found in the query list.
  * [optional] Repacking the final output to make the file contiguous on storage

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
  --repack, REPACK  repack after changing the file, yes or no
Example:
--------
.. highlight:: c

Prepare input::

 cat input_sample.txt

  /global/cscratch1/sd/jialin/h5boss/3665-55247.hdf5

  ...

 cat pmf_update.txt

  plates mjds fibers

  6697 56419 796

  4697 55660 190

  4191 55444 636
  
  ...

Download: :download:`input_sample.txt <_static/input_sample.txt>`, :download:`pmf_update.txt <_static/pmf_update.txt>`, :download:`base.h5 <_static/base.h5>`

Execute command::

 update base.h5 input_sample.txt pmf_update.txt  --repack=yes

Output::

 Will repack the file for better storage layout afterwards.
 Query: Plates/Mjds/Fibers: 11
 Input: 2393 hdf5 files
 Output: base.h5 
 Running Updating:
 Query time: 0.00 seconds
 plates/mjds/fibers to be added: 10
 Running selection:
 -Source file open: 1.93
 -Fiber query time: 0.00
 -Fiber copy time: 0.20
 -Catalog copy time: 0.83
 -Group create time: 0.00
 -File close time: 0.04
 Selection Time: 5.15 seconds
 plates/mjds/fibers to be removed: 6
 Running removing:
 Removed 6 plates/mjds/fibers,Skipped 0
 Remvoing Time: 0.02 seconds
 Running repacking:
 Repacking Time: 2.33 seconds
 Updating complete: 8.40 seconds
