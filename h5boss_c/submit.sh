#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 3 
#SBATCH -t 00:10:00
#SBATCH -J ch5boss
#SBATCH -e %j.err
#SBATCH -o %j.out
template=$SCRATCH/bosslover/scaling-test/1k_template.h5
output=$SCRATCH/bosslover/scaling-test/test.h5
cori_output=/global/cscratch1/sd/jialin/bosslover/scaling-test/10k_template_early.h5
cori_ost72_output=/global/cscratch1/sd/jialin/bosslover/scaling-test/ost72/10k_template_early.h5
srun -n 96 ./subset.exe -f $cori_output -m nodes10k.txt
