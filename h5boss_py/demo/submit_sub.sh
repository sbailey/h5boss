#!/bin/bash
#SBATCH -p regular
#SBATCH -N 1
#SBATCH -t 00:20:00
#SBATCH -J subset
#SBATCH -e %j_1k.err
#SBATCH -o %j_1k.out

cd $SLURM_SUBMIT_DIR

srun -n 10 python-mpi ../scripts/subset.py input-full $SCRATCH/output_1k.h5 pmf-list/pmf1k 
