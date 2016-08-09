#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 4
#SBATCH -t 00:05:00
#SBATCH -J h5boss
#SBATCH -e h5boss%j.err
#SBATCH -o h5boss%j.out
srun -n 100 ./subset.exe -f $SCRATCH/bosslover/scaling-test/1k_h5boss.h5 -m nodes1k.txt
