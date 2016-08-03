#!/bin/bash
#SBATCH -p regular 
#SBATCH -N 1
#SBATCH -t 00:50:00
#SBATCH -J subset-serial-bb
#SBATCH -e %j_1k.err
#SBATCH -o %j_1k.out
#SBATCH -A mpccc
#DW jobdw capacity=4420GB access_mode=striped type=scratch
#DW stage_in source=/global/cscratch1/sd/jialin/h5boss destination=$DW_JOB_STRIPED/ type=directory

SCRDIR=$DW_JOB_STRIPED
module load lustre-cray_ari_s
module load dws

cd $SLURM_SUBMIT_DIR
subset input-full-bb $SCRDIR/1k_aug3.h5 pmf-list/pmf1k
