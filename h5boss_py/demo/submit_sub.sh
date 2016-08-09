#!/bin/bash
#SBATCH -p debug
#SBATCH -N 7 
#SBATCH -t 00:05:00
#SBATCH -J subset-mpi
#SBATCH -e %j_1k.err
#SBATCH -o %j_1k.out
#SBATCH -L SCRATCH
cd $SLURM_SUBMIT_DIR

#option 1: subfiling
#srun -n 200 python-mpi ../scripts/subset_mpi-sf.py input-full $SCRATCH/bosslover/parallel-test/newt_1k.h5 pmf-list/pmf1k --mpi="yes"

#option 2: single shared file
output=$SCRATCH/bosslover/scaling-test/1k_single_aug8.h5
#rm $output
template=$SCRATCH/bosslover/scaling-test/1k_template.h5 
cp $template $output
srun -n 200 python ../scripts/subset_mpi.py input-full-cori $output pmf-list/pmf1k --mpi="yes"
