.. _fits2hdf:

Convertion
==========
This section shows the mapping between Fits and HDF5 formats, and following with the design of H5Boss :ref:`Formats, <h5bossfmts>`


Fits to HDF51

Catalog:

===============================    ========  ===============  ============
Fits File                          Fits HDU  HDF5 Group       HDF5 Dataset
===============================    ========  ===============  ============
photoMatchPlate-pppp-mmmmm.fits    HDU 1     plate/mjd/photo  match
photoPosPlate-pppp-mmmmm.fits 	   HDU 1     plate/mjd/photo  matchpos
photoPlate-pppp-mmmmm.fits         HDU 1     plate/mjd/photo  matchflux
v5_7_0/spZbest-pppp-mmmmm.fits     HDU 1     plate/mjd        zbest
v5_7_0/spZline-pppp-mmmmm.fits     HDU 1     plate/mjd        zline
spPlate-pppp-mmmmm.fits            HDU 5     plate/mjd        plugmap
===============================    ========  ===============  ============

Spectra:

== ================================ ================ =================================     ============
id Fits File                        Fits HDU         HDF5 Group       			   HDF5 Dataset
== ================================ ================ =================================     ====================
1  spPlate-pppp-mmmmm.fits          HDU 0            plate/mjd/ffff   			   coadd(col2) FLUX 
2  spPlate-pppp-mmmmm.fits          HDU 1 IVAR       plate/mjd/ffff   			   coadd(col3) IVAR
3  spPlate-pppp-mmmmm.fits          HDU 2 ANDMASK    plate/mjd/ffff   			   coadd(col4) AND_MASK
4  spPlate-pppp-mmmmm.fits          HDU 3 ORMASK     plate/mjd/ffff   			   coadd(col5) OR_MASK    
5  spPlate-pppp-mmmmm.fits          HDU 4 WAVEDISP   plate/mjd/ffff   			   coadd(col6) WAVEDISP
6  spPlate-pppp-mmmmm.fits          HDU 5 PLUGMAP    plate/mjd/ffff                        coadd(col1) 
7  spPlate-pppp-mmmmm.fits          HDU 6 SKY        plate/mjd/ffff   			   coadd(col7)
8                                                    plate/mjd/ffff                        coadd(col8)*
9  spCFrame-[br][12]-[0-9]{8}.fits  HDU 0            plate/mjd/ffff/exposures/eeeeeeee     b/r(col1)
10 spCFrame-[br][12]-[0-9]{8}.fits  HDU 1 IVAR       plate/mjd/ffff/exposures/eeeeeeee     b/r(col2)
11 spCFrame-[br][12]-[0-9]{8}.fits  HDU 2 MASK       plate/mjd/ffff/exposures/eeeeeeee     b/r(col3)
12 spCFrame-[br][12]-[0-9]{8}.fits  HDU 3 WAVELENGTH plate/mjd/ffff/exposures/eeeeeeee     b/r(col4)*
13 spCFrame-[br][12]-[0-9]{8}.fits  HDU 4 WAVEDISP   plate/mjd/ffff/exposures/eeeeeeee     b/r(col5)
14 spCFrame-[br][12]-[0-9]{8}.fits  HDU 6 SKY        plate/mjd/ffff/exposures/eeeeeeee     b/r(col6)
15 spCFrame-[br][12]-[0-9]{8}.fits  HDU 7 X          plate/mjd/ffff/exposures/eeeeeeee     b/r(col7)
16 spCFrame-[br][12]-[0-9]{8}.fits  HDU 8 SUPERFLAT  plate/mjd/ffff/exposures/eeeeeeee     b/r(col8)*
17 spFlat-[br][12]-[0-9]{8}.fits.gz HDU 0 FIBERFLAT  plate/mjd/ffff/exposures/eeeeeeee     b/r(col8)*
== ================================ ================ =================================     ============

Notes:

line *12*,wavelength is log based, so the conversion code calculates the reverse, i.e., 10^wavelength 

line *16* and *17*, 
 
.. highlight:: c


Example:


.. _myfits2h5-v1:

.. figure:: images/fits2fmt1.png
   :alt: Fits to H5Boss format 1
   :align: left

   Fits to H5Boss Format v1
