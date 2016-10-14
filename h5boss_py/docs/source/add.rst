.. _add:
Add
========

Usage:
------
Given a plate/mjd/fiber query list. This `add` command will compare the existing plate/mjd/fibers in the base hdf5 file with this query, then search the new plate/mjd/fiber (which are not existed in the base hdf5 file) from the input hdf5 files, and then add the founded plate/mjd/fiber into the base file.

The base file is supposed to be augmented with a few new plate/mjd/fibers. 

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

execute command::

 >add base.h5 input_sample.txt pmf_sample.txt

