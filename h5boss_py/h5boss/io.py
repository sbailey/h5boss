import os.path
import numpy as np
from astropy.io import fits
from astropy.table import Table

def load_coadds(platefile, zbestfile=None, run1d=None):
    '''
    Document ...
    '''
    #- Load spPlate data
    fx = fits.open(platefile, memmap=False)
    header   = fx[0].header
    c0       = header['COEFF0']
    c1       = header['COEFF1']
    nwave    = header['NAXIS1']
    nfiber   = header['NAXIS2']
    wave     = (10**(c0 + c1*np.arange(nwave))).astype(np.float32)
    flux     = fx[0].data
    ivar     = fx[1].data
    and_mask = fx[2].data
    or_mask  = fx[3].data
    wavedisp = fx[4].data
    sky      = fx[6].data
    fx.close()

    if run1d is None:
        run1d = header['RUN2D']  #- default run1d == run2d
    
    #- Get best fit model from zbest file
    if zbestfile is None:
        zbestfile = platefile.replace('spPlate', '{}/spZbest'.format(run1d))

    model = fits.getdata(zbestfile, 2)

    coadds = list()
    for i in range(nfiber):
        sp = Table()
        sp['WAVE']     = wave               #- repeat !
        sp['FLUX']     = flux[i]
        sp['IVAR']     = ivar[i]
        sp['AND_MASK'] = and_mask[i]
        sp['OR_MASK']  = or_mask[i]
        sp['WAVEDISP'] = wavedisp[i]
        sp['SKY']      = sky[i]
        sp['MODEL']    = model[i]
        sp.meta = header
        
        #- TODO: Add units, comments to each column
        
        coadds.append(sp)
        
    return coadds

def load_frame(framefile, cframefile=None, flatfile=None):
    """
    Document ...
    """
    if cframefile is None:
        cframefile = framefile.replace('spFrame', 'spCFrame')
        if cframefile.endswith('.gz'):
            cframefile = cframefile[:-3]

    #- Load framefile and get original dimensions
    eflux = fits.getdata(framefile, 0)
    nfiber, npix = eflux.shape
            
    #- Load spCFrame file; trim arrays back to original size
    fx = fits.open(cframefile, memmap=False)
    header = fx[0].header
    flux = fx[0].data[:, 0:npix]
    ivar = fx[1].data[:, 0:npix]
    mask = fx[2].data[:, 0:npix]
    wave = (10**fx[3].data[:, 0:npix]).astype(np.float32)
    wavedisp  = fx[4].data[:, 0:npix]
    sky    = fx[6].data[:, 0:npix]
    x      = fx[7].data[:, 0:npix]
    superflat = fx[8].data[:, 0:npix]
    
    #- Load fiberflat spFlat[0]
    if flatfile is None:
        flatfile = header['FLATFILE'].replace('sdR', 'spFlat')
        flatfile = flatfile.replace('.fit', '.fits.gz')
        filedir, basename = os.path.split(os.path.abspath(cframefile))
        flatfile = os.path.join(filedir, flatfile)

    fiberflat = fits.getdata(flatfile, 0)
    
    #- Calculate calibration vector: flux = electrons * calib
    electrons = eflux * fiberflat * superflat
    ii = np.where(electrons != 0.0)
    calib = np.zeros(flux.shape)
    calib[ii] = flux[ii] / electrons[ii]
            
    fx.close()
    
    #- Assemble spectra tables
    spectra = list()
    for i in range(nfiber):
        sp = Table()
        sp['WAVE'] = wave[i]
        sp['FLUX'] = flux[i]
        sp['IVAR'] = ivar[i]
        sp['MASK'] = mask[i]
        sp['WAVEDISP'] = wavedisp[i]
        sp['SKY'] = sky[i]
        sp['X'] = x[i]
        sp['CALIB'] = calib[i].astype(np.float32)
        sp.meta = header
        
        #- TODO: Add units, comments to each column
        
        spectra.append(sp)
        
    return spectra
    
    
    
    
    
    
    
