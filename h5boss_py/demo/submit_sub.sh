#!/bin/bash
#SBATCH -p regular 
#SBATCH -N 1
#SBATCH -t 01:00:00
#SBATCH -J subset-mpi
#SBATCH -e %j_100k.err
#SBATCH -o %j_100k.out
#SBATCH -L SCRATCH
cd $SLURM_SUBMIT_DIR
template=$SCRATCH/bosslover/scaling-test/ost72/100k_py_template32.h5 
srun -n 32 python-mpi ../scripts/subset_mpi.py input-full-cori $template pmf-list/large-scale/pmf100k-shuffle.csv --mpi="yes" --template="all"
