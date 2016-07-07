#!/bin/bash
#SBATCH -p debug
#SBATCH -N 2
#SBATCH -t 00:10:00
#SBATCH -J subset-mpi
#SBATCH -e %j_1k.err
#SBATCH -o %j_1k.out

cd $SLURM_SUBMIT_DIR

srun -n 20 python-mpi ../scripts/subset_mpi.py input-full $SCRATCH/output_10.jul3.h5 pmf-list/pmf10k --mpi="yes" 
