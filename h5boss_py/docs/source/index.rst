.. h5boss documentation master file, created by
   sphinx-quickstart on Tue Oct 11 12:04:08 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome!
========

H5Boss is an exploratory python tool for managing BOSS spectra data, SDSS-II. 

Boss is originally maintained as millions of fits file in thousands of different folders. Accessing and analyzing them are inefficient in terms of I/O bandwidth and programming productivity. In h5boss, we developed functions to support:

* Reformatting: Preserve the fits file structure and spectrum hierarchicy using HDF5
* Subsetting: Support subset/add/update operation, to extract selected 'plate/mjd/fiber' and save in one HDF5 file

Currently, h5boss is implemented in both python and c version, in which the python version is actively maintained and supported. The c version is mainly for I/O sensitive users/applications. 

Quickstart:
===========

* :ref:`Installation <install>`

Formats:
========
  
* :ref:`Fits->Hdf5 <fits2hdf>`
* :ref:`Design <h5bossfmts>`
 
Commands:
=============

* :ref:`Convert <convert>`
* :ref:`Subset <subset>`
* :ref:`Add <add>`
* :ref:`Update <update>`


Modules:
========

* :ref:`H5boss <modules>`

Missing Features:
=================

* :ref:`H5bossdev <h5bossdev>`

Indices:
========

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

