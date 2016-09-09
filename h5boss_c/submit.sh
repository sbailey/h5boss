#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 1
#SBATCH -t 00:30:00
#SBATCH -J ch5boss
#SBATCH -e %j.err
#SBATCH -o %j.out
coriost72output=/global/cscratch1/sd/jialin/bosslover/scaling-test/ost72/10k_sep8.1.h5
srun -n 32  ./subset.exe -f /global/cscratch1/sd/jialin/bosslover/scaling-test/ost72/10k_sep8.1.h5 -m 2968390_nodes10k_fiber.txt -n 93538 -l 2968390_nodes10k_catalog.txt -k 9750 
