#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 1 
#SBATCH -t 00:10:00
#SBATCH -J ch5boss
#SBATCH -e %j.err
#SBATCH -o %j.out
coriost72output=/global/cscratch1/sd/jialin/bosslover/scaling-test/ost72/10k_py_template4.h5
srun -n 32  ./subset.exe -f /global/cscratch1/sd/jialin/bosslover/scaling-test/ost72/10k_py_template1.h5 -m nodes10k_fiber.txt -n 188000 -l nodes10k_catalog.txt -k 19500 
