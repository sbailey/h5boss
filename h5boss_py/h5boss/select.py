import numpy as np
import h5py

def select(infiles, outfile, plates, mjds, fibers):
    '''
    Select a set of (plates,mjds,fibers) from a set of input files
    
    Args:
        infiles : list of input filenames, or single filename
        outfile : output file to write the selection
        plates : list of plates
        mjds : list of plates
        fibers : list of fibers        
    '''
    plates = np.asarray(plates)
    mjds = np.asarray(mjds)
    fibers = np.asarray(fibers)
    
    if not isinstance(infiles, (list, tuple)):
        infiles = [infiles,]
        
    hx = h5py.File(outfile)
        
    for infile in infiles:
        fx = h5py.File(infile, mode='r')
        for plate in fx.keys():
            for mjd in fx[plate].keys():
                ii = (plates == int(plate)) & (mjds == int(mjd))
                xfibers = fibers[ii]
                for fiber in xfibers:
                    id = '{}/{}/{}'.format(plate, mjd, fiber)
                    # hx[id] = fx[id].copy()
		    parent_id='{}/{}'.format(plate, mjd)
                    hx.create_group(parent_id)
                    fx.copy(id, hx[parent_id])
                
                for name in ['plugmap', 'zbest', 'zline',
                    'photo/match', 'photo/matchflux', 'photo/matchpos']:
                    id = '{}/{}/{}'.format(plate, mjd, name)
                    catalog = fx[id]
                    jj = np.in1d(catalog['FIBERID'], xfibers)
                    hx[id] = fx[id][jj].copy()
                    
    hx.close()
