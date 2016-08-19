#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 1
#SBATCH -t 00:15:00
#SBATCH -J subset-mpi
#SBATCH -e %j_1k.err
#SBATCH -o %j_1k.out
#SBATCH -L SCRATCH
cd $SLURM_SUBMIT_DIR

#option 1: subfiling
#srun -n 200 python-mpi ../scripts/subset_mpi-sf.py input-full $SCRATCH/bosslover/parallel-test/newt_1k.h5 pmf-list/pmf1k --mpi="yes"

#option 2: single shared file
output=$SCRATCH/bosslover/scaling-test/1k_py_p2.1.h5
#rm $output
template=$SCRATCH/bosslover/scaling-test/1k_pyh5boss_fiber_early_catalog_early_template.h5 
#cp $template $output
#rm $template >/dev/null
#srun -n 32 python-mpi ../scripts/subset_mpi.py input-full-cori $template pmf-list/pmf1k --mpi="yes" --template="yes"
srun -n 32 python-mpi ../scripts/subset_mpi.py input-full-cori $template pmf-list/pmf1k --mpi="yes" --template="no"
