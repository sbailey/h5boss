#!/bin/bash
#SBATCH -p regular
#SBATCH -N 103
#SBATCH -t 01:00:00
#SBATCH -J fits2hdf-parallel
#SBATCH -e %j.err
#SBATCH -o %j.out
#SBATCH --mail-user=jalnliu@lbl.gov
#SBATCH --mail-type=ALL

cd $SLURM_SUBMIT_DIR
#module load python/2.7-anaconda
#module list
srun -n 2464 python-mpi boss2hdf5-parallel.py 
