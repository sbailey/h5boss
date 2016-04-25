#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 1
#SBATCH -t 00:30:00
#SBATCH -J fits2hdf-parallel
#SBATCH -e %j.err
#SBATCH -o %j.out

cd $SLURM_SUBMIT_DIR
module list
srun -n 32 python-mpi boss2hdf5-parallel.py 
