#!/bin/bash
#SBATCH -p regular
#SBATCH -N 1
#SBATCH -t 00:10:00
#SBATCH -J subset-serial-bb
#SBATCH -e %j_100k.err
#SBATCH -o %j_100k.out
#SBATCH -A mpccc
#DW jobdw capacity=212GB access_mode=striped type=scratch
SCRDIR=$DW_JOB_STRIPED
module load lustre-cray_ari_s
module load dws

cd $SLURM_SUBMIT_DIR
TESTDIR=$SCRDIR/bosslover/scaling-test/
rm -rf TESTDIR
mkdir -p $TESTDIR || exit
subset input-full $TESTDIR/pmf100-s.h5 pmf-list/pmf100
