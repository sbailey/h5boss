#!/bin/bash
#SBATCH -p debug
#SBATCH -N 10
#SBATCH -t 00:20:00
#SBATCH -J subset-mpi
#SBATCH -e %j_100k.err
#SBATCH -o %j_100k.out

cd $SLURM_SUBMIT_DIR

srun -n 200 python-mpi ../scripts/subset_mpi-sf.py input-full $SCRATCH/bosslover/newt_200_100k.h5 pmf-list/pmf100k --mpi="yes"
