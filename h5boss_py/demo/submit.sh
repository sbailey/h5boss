#!/bin/bash
#SBATCH -p regular
#SBATCH -N 1
#SBATCH -t 00:10:00
#SBATCH -J subset-serial
#SBATCH -e %j_1k.err
#SBATCH -o %j_1k.out
cd $SLURM_SUBMIT_DIR
SCRATCH_A=/project/projectdirs/mpccc/jialin
TESTDIR=$SCRATCH_A/bosslover/scaling-test/
subset input-full-project $TESTDIR/1k_cmp_project.h5 pmf-list/pmf1k
