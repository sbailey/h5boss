.. _psubset:
Parallel Subset
===============

Usage:
------
.. highlight:: c 

usage::

 subset_mpi [-h] [--template TEMPLATE] [--mpi MPI] [--fiber FIBER]

                  [--catalog CATALOG] [--datamap DATAMAP]

                  input output pmf

positional arguments::

  input                HDF5 input list

  output               HDF5 output

  pmf                  Plate/mjd/fiber list

optional arguments::

  -h, --help           show this help message and exit

  --template TEMPLATE  Create template only,yes/no/all

  --mpi MPI            using mpi yes/no

  --fiber FIBER        specify fiber csv output

  --catalog CATALOG    specify catalog csv output

  --datamap DATAMAP    specify datamap pickle file


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

download: :download:`input <_static/input_sample.txt>`, :download:`pmf <_static/pmf_sample.txt>`

execute command::

 >subset_mpi input_sample.txt output.h5 pmf_sample.txt



