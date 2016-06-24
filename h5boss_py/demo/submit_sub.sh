#!/bin/bash
#SBATCH -p regular
#SBATCH -N 1
#SBATCH -t 03:00:00
#SBATCH -J subset
#SBATCH -e %j_100k.err
#SBATCH -o %j_100k.out

cd $SLURM_SUBMIT_DIR

subset input-full $SCRATCH/output_100k.h5 pmf-list/pmf100k 
