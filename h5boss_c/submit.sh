#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 1 
#SBATCH -t 00:10:00
#SBATCH -J ch5boss
#SBATCH -e %j.err
#SBATCH -o %j.out
template=$SCRATCH/bosslover/scaling-test/1k_template.h5
output=$SCRATCH/bosslover/scaling-test/test.h5
cori_output=/global/cscratch1/sd/jialin/bosslover/scaling-test/10k_template_early.h5
cori_ost72_output=/global/cscratch1/sd/jialin/bosslover/scaling-test/ost72/10k_py_template1.h5
#/global/cscratch1/sd/jialin/bosslover/scaling-test/ost72
srun -n 32 ./subset.exe -f $cori_ost72_output -m nodes10k_fiber.txt

