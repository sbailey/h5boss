import sys, os
import numpy as np
from astropy.io import fits
from astropy.table import Table
import h5boss.io
import time

def serial_convert(platefile,hdf5output):
    platefile=platefile[0]
    if not os.path.isfile(platefile):
     print("%s not existing"%platefile)
     sys.exit(0)
    hdf5output=str(hdf5output)
    print ("Output:%s"%hdf5output)
    print ("Running Conversion:")
    filedir = os.path.split(os.path.abspath(platefile))[0]
    hdr = fits.getheader(platefile)
    plate = hdr['PLATEID']
    mjd = hdr['MJD']
    tstart=time.time()
    #--- Plugmap ---
    print('plugmap')
    plugmap = Table.read(platefile, 5)
    dataname = '{}/{}/plugmap'.format(plate, mjd)
    plugmap.write(hdf5output, path=dataname, append=True)

    #--- zbest ---
    print('zbest')
    run1d = hdr['RUN2D']  #- default run1d == run2d
    zbestfile = platefile.replace('spPlate', '{}/spZbest'.format(run1d))
    zbest = Table.read(zbestfile, 1)
    dataname = '{}/{}/zbest'.format(plate, mjd)
    zbest.write(hdf5output, path=dataname, append=True)
    nfiber = len(zbest)

    #--- zall (skip) ---
    pass

    #--- zline ---
    print('zline')
    zlinefile = zbestfile.replace('spZbest-', 'spZline-')
    zline = Table.read(zlinefile, 1)
    dataname = '{}/{}/zline'.format(plate, mjd)
    zline.write(hdf5output, path=dataname, append=True)

    #--- photometric matches ---
    print('photo')
    photomatchfile = platefile.replace('spPlate-', 'photoMatchPlate-')
    photomatch = Table.read(photomatchfile, 1)
    photomatch['FIBERID'] = np.arange(1, nfiber+1, dtype=np.int16)
    dataname = '{}/{}/photo/match'.format(plate, mjd)
    photomatch.write(hdf5output, path=dataname, append=True)

    photoposfile = platefile.replace('spPlate-', 'photoPosPlate-')
    photopos = Table.read(photoposfile, 1)
    photopos['FIBERID'] = np.arange(1, nfiber+1, dtype=np.int16)
    dataname = '{}/{}/photo/matchpos'.format(plate, mjd)
    photopos.write(hdf5output, path=dataname, append=True)

    photofluxfile = platefile.replace('spPlate-', 'photoPlate-')
    photoflux = Table.read(photofluxfile, 1)
    photoflux['FIBERID'] = np.arange(1, nfiber+1, dtype=np.int16)
    dataname = '{}/{}/photo/matchflux'.format(plate, mjd)
    photoflux.write(hdf5output, path=dataname, append=True)

    #--- Coadd ---
    print('loading coadds')
    coadds = h5boss.io.load_coadds(platefile)

    print('writing coadds')
    for i, cx in enumerate(coadds):
        dataname = '{}/{}/{}/coadd'.format(plate, mjd, i+1)
        cx.write(hdf5output, path=dataname, append=True)
#    h5boss.io.write_coadds_vstack(platefile, plate,mjd,hdf5output)

    #--- Individual exposures ---
    #- Parse spPlancomb to get exposures that were used
    print('parsing planfile')
    planfile = platefile.replace('spPlate-', 'spPlancomb-').replace('.fits', '.par')
    framefiles = list()
    for line in open(planfile):
        if line.startswith('SPEXP '):
            tmp = line.split()
            tmp = [x+'.gz' for x in tmp[7:-1]]
            framefiles.extend(tmp)

    print('copying individual exposure')
    for filename in framefiles:
        print(filename)
        frame = h5boss.io.load_frame(filedir+'/'+filename)
        if ('spFrame-b1' in filename) or ('spFrame-r1' in filename):
            offset = 0
        elif ('spFrame-b2' in filename) or ('spFrame-r2' in filename):
            offset = 500
        else:
            print('huh?', filename)
            sys.exit(1)

        for i, fx in enumerate(frame):
            br = fx.meta['CAMERAS'][0]
            expid = fx.meta['EXPOSURE']
            fiber = offset+i+1
            dataname = '{}/{}/{}/exposures/{}/{}'.format(plate, mjd, fiber, expid, br)
            fx.write(hdf5output, path=dataname, append=True)
#    print('writing exposures')
#    h5boss.io.write_frame_vstack(filedir,framefiles,plate,mjd,hdf5output)

    tend=time.time()-tstart
    print ('Conversion time: %.2f seconds'%tend)
