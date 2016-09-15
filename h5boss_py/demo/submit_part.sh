#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 1
#SBATCH -t 00:10:00
#SBATCH -J boss2hdf
#SBATCH -e %j.err
#SBATCH -o %j.out
#SBATCH --mail-user=jalnliu@lbl.gov
#SBATCH --mail-type=ALL
cd $SLURM_SUBMIT_DIR
#module load python/2.7-anaconda
#module list
srun -n 4 python-mpi boss2hdf5-parallel.py --output /global/cscratch1/sd/jialin/h5boss_v2/
