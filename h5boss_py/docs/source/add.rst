.. _add:
Add
========
Given a plate/mjd/fiber query list. This `add` command will update the base hdf5 accordingly. Basically, add will
  * Compare the existing plate/mjd/fibers in the base hdf5 file with this query,
  * Search the new plate/mjd/fiber, which are not existed in the base hdf5 file, from the input hdf5 files
  * Add the founded plate/mjd/fiber into the base file

The base file is supposed to be augmented with a few new plate/mjd/fibers.

Usage:
------

.. highlight:: c 

add -h

usage::
 
  add [-h] base input pmf

positional arguments::

  base        Pre-subseted HDF5 file

  input       HDF5 input files list

  pmf         Plate/mjd/fiber list

optional arguments::

  -h, --help  show this help message and exit

Example:
--------
.. highlight:: c

Prepare input::

 cat input_sample.txt

  /global/cscratch1/sd/jialin/h5boss/3665-55247.hdf5

  ...

 cat pmf_add.txt

  plates mjds fibers

  3665 55247 65

  3665 55247 390

  ...

Download: :download:`input_sample.txt <_static/input_sample.txt>`, :download:`pmf_add.txt <_static/pmf_add.txt>`, :download:`base.h5 <_static/base.h5>`

Execute command::

 add base.h5 input_sample.txt pmf_add.txt

Output::

 -Source file open: 2.28
 -Fiber query time: 0.00
 -Fiber copy time: 0.21
 -Catalog copy time: 0.84
 -Group create time: 0.00
 -File close time: 0.04
 Selection Time: 7.43 seconds
 Done selection


