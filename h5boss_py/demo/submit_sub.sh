#!/bin/bash
#SBATCH -p debug
#SBATCH -N 9
#SBATCH -t 00:05:00
#SBATCH -J subset-mpi
#SBATCH -e %j_1k.err
#SBATCH -o %j_1k.out

cd $SLURM_SUBMIT_DIR

srun -n 200 python-mpi ../scripts/subset_mpi-sf.py input-full $SCRATCH/bosslover/scaling-test/newt_1k.h5 pmf-list/pmf1k --mpi="yes"
