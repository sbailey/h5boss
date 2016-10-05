import h5py 
import cPickle as pickle
from mpi4py import MPI
import argparse
from h5boss.selectmpi_v1 import create_template

def test_create():
    parser = argparse.ArgumentParser(prog='template_create')
    parser.add_argument("input",  help="pickle input")
    parser.add_argument("output", help="HDF5 output")
    opts=parser.parse_args()

    global_fiber = opts.input
    outfile = opts.output
    comm=MPI.COMM_WORLD
    nproc = comm.Get_size()
    rank = comm.Get_rank()
    gf=pickle.load(open(global_fiber,"rb"))
    t1=MPI.Wtime()
    if rank==0:
       create_template(outfile,gf,'fiber',rank)
    t2=MPI.Wtime()
    if rank==0:
       print("template creation cost %.2f"%(t2-t1))
if __name__=='__main__':
    test_create()
