#!/bin/bash
#SBATCH -p debug
#SBATCH -N 34
#SBATCH -t 00:05:00
#SBATCH -J subset-mpi
#SBATCH -e %j_100k.err
#SBATCH -o %j_100k.out

cd $SLURM_SUBMIT_DIR

srun -n 800 python-mpi ../scripts/subset_mpi-sf.py input-full $SCRATCH/bosslover/newt_800_1k.h5 pmf-list/pmf1k --mpi="yes"
