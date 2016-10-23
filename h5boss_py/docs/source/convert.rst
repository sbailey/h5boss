.. _convert:
Convert
========

Usage:
------
Convert boss data from fits to hdf5 format

.. highlight:: c

At NERSC, BOSS data are maintained in `Fits <http://fits.gsfc.nasa.gov/fits_documentation.html>`_ format and are stored on global project:: 

/global/projecta/projectdirs/sdss/data/sdss/dr12/boss/spectro/redux/v5_7_0/

H5Boss offeres two alternative hdf5 formats, v1 and v2. The two formats are essentially designed to ease the file management and speedup the I/O. The two formats differ in the way how the fiber is organized, etc. More details can be found at :ref:`Design <h5bossfmts>`

We have converted all Fits files into HDF5, which has largely reduced the file number from ~1 million to 2500. Follow the steps below to convert 1 Fits file into HDF5 file. 

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

 >export BOSS_DIR=/global/projecta/projectdirs/sdss/data/sdss/dr12/boss/spectro/redux/v5_7_0/
 >boss2hdf5_v1 -i $BOSS_DIR/4444/spPlate-4444-55538.fits -o 4444-55538_v1.h5


