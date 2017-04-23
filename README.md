# H5Boss
H5Boss is an exploratory python tool for managing BOSS spectra data, SDSS-II.

Boss is originally maintained as millions of fits file in thousands of different folders. Accessing and analyzing them are inefficient in terms of I/O bandwidth and programming productivity. In h5boss, we developed functions to support:

  1. Reformatting: Preserve the fits file structure and specture hierarchicy using HDF5
  2. Subsetting: Support subset/add/update operation, to extract selected ‘plate/mjd/fiber’ and save in one HDF5 file

Currently, h5boss is implemented in both python and c version, in which the python version is actively maintained and supported. The c version is mainly for I/O sensitive users/applications.

# Tutorial
1. download repo
2. cd h5boss_py/docs/
3. make html
4. open build/html/index.html

# Demo with h5boss_py
1. cd h5boss_py/demo
2. subset -h
3. add -h
4. update -h

# Demo with h5boss_c
1. cd h5boss_c
2. make
