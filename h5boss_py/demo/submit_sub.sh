#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 4
#SBATCH -t 00:20:00
#SBATCH -J subset-mpi
#SBATCH -e %j_10k.err
#SBATCH -o %j_10k.out
#SBATCH -L SCRATCH
cd $SLURM_SUBMIT_DIR
template=$SCRATCH/bosslover/scaling-test/ost72/10k_py_template128.h5 
srun -n 128 python-mpi ../scripts/subset_mpi.py input-full-cori $template pmf-list/large-scale/pmf10k-shuffle.csv --mpi="yes" --template="all"
