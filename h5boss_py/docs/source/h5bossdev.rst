.. _h5bossdev:

Missing Features/Funcionts
==========================

This page documents the missing features/functions in various versions of the h5boss package. Further development: `Github:H5boss-dev <https://github.com/valiantljk/h5boss-dev>`_. 

H5boss python **serial** package for format version **1**::

 This version is complete
 Support all features: convert/subset/add/update

H5boss python **parallel** package for format version **1**::

 Support convert/subset in parallel
 Not support add/update

H5boss python **serial** package for format version **2** ::

 Support convert
 
H5boss python **parallel** package for format version **2** ::

 Support convert/subset(fiber only)
 Not support add/update and catalog subset
 
H5boss c **parallel** package for format version **1** :: 

 Support subset (fiber only), and requires a pre-created template
