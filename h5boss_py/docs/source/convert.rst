.. _convert:
Convert
========
Convert the boss data from `Fits <http://fits.gsfc.nasa.gov/fits_documentation.html>`_  to `HDF5 <https://support.hdfgroup.org/HDF5/Tutor/introductory.html>`_ format

At NERSC, BOSS data are stored on global projecta file system:: 

/global/projecta/projectdirs/sdss/data/sdss/dr12/boss/spectro/redux/v5_7_0/

H5Boss offeres two alternative hdf5 formats, v1 and v2. The two formats are essentially designed to ease the file management and speedup the I/O. The two formats differ in the way how the fibers are organized, etc. More details can be found at :ref:`Design <h5bossfmts>`

We have converted all Fits files into HDF5 formats, which has largely reduced the number of files from ~1 million to 2500. Follow the steps below to convert all Fits file of plate `4444` and mjd `55538` into a single HDF5 file, named `4444-55538_v1.h5`.

Usage:
------

.. highlight:: c

Usage::

  boss2hdf5_v1 [options] or boss2hdf5_v2 [options]

Options::

  -h, --help            show this help message and exit

  -i INPUT, --input=INPUT     input spPlate file

  -o OUTPUT, --output=OUTPUT  output hdf5 file



Example:
--------
.. highlight:: c

Execute command::

 export BOSS_DIR=/global/projecta/projectdirs/sdss/data/sdss/dr12/boss/spectro/redux/v5_7_0/
 boss2hdf5_v1 -i $BOSS_DIR/4444/spPlate-4444-55538.fits -o $SCRATCH/4444-55538_v1.h5

This command not only converts the specified fits file, i.e., spPlate-4444-55538.fits, but also scan other related fits file in the same directory, $BOSS_DIR/4444. The detailed conversion can be found at :ref:`Design Fits2hdf <fits2hdf>`

Output::

 Running Conversion:
 plugmap
 zbest
 zline
 photo
 loading coadds
 writing coadds
 parsing planfile
 copying individual exposure
 spFrame-b1-00123585.fits.gz
 spFrame-b2-00123585.fits.gz
 spFrame-r1-00123585.fits.gz
 spFrame-r2-00123585.fits.gz
 spFrame-b1-00123586.fits.gz
 spFrame-b2-00123586.fits.gz
 spFrame-r1-00123586.fits.gz
 spFrame-r2-00123586.fits.gz
 spFrame-b1-00123587.fits.gz
 spFrame-b2-00123587.fits.gz
 spFrame-r1-00123587.fits.gz
 spFrame-r2-00123587.fits.gz
 spFrame-b1-00123588.fits.gz
 spFrame-b2-00123588.fits.gz
 spFrame-r1-00123588.fits.gz
 spFrame-r2-00123588.fits.gz
 spFrame-b1-00123589.fits.gz
 spFrame-b2-00123589.fits.gz
 spFrame-r1-00123589.fits.gz
 spFrame-r2-00123589.fits.gz
 Conversion time: 1521.86 seconds
