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

execute command::

 >update base.h5 input_sample.txt pmf_sample.txt

