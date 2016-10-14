.. _convert:
Convert
========

Usage:
------
Convert boss data from fits to hdf5 format

.. highlight:: c

At NERSC, BOSS data is stored at:: 

/global/projecta/projectdirs/sdss/data/sdss/dr12/boss/spectro/redux/v5_7_0/

There are two alternative hdf5 formats, v1 and v2. Their difference can be seen at :ref:`Design <h5bossfmts>`

Usage::

  boss2hdf5_v1 [options] or boss2hdf5_v2 [options]

Options::

  -h, --help            show this help message and exit

  -i INPUT, --input=INPUT     input spPlate file

  -o OUTPUT, --output=OUTPUT  output hdf5 file



Example:
--------
.. highlight:: c

execute command::

 >boss2hdf5_v1 spPlate-4444-55538.fits 4444-55538_v1.h5
