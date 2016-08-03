#!/bin/bash
#SBATCH -p debug
#SBATCH -N 1
#SBATCH -t 00:18:00
#SBATCH -J subset-mpi
#SBATCH -e %j_1k.err
#SBATCH -o %j_1k.out

cd $SLURM_SUBMIT_DIR

#option 1: subfiling
#srun -n 200 python-mpi ../scripts/subset_mpi-sf.py input-full $SCRATCH/bosslover/parallel-test/newt_1k.h5 pmf-list/pmf1k --mpi="yes"

#option 2: single shared file
srun -n 20 python-mpi ../scripts/subset_mpi.py input-full $SCRATCH/bosslover/scaling-test/20_single_aug3.h5 pmf-list/pmf20 --mpi="yes"
