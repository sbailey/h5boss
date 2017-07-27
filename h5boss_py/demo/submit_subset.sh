#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 1
#SBATCH -t 00:15:00
#SBATCH -J subset-mpi
#SBATCH -e %j.err
#SBATCH -o %j.out
#SBATCH -L SCRATCH
cd $SLURM_SUBMIT_DIR

# Control Arguments:
version="_v1" # or "_v2"
cmdscript="../scripts/subset_mpi"$version".py "
nproc="24"
cmd="srun -n "$nproc" python-mpi "$cmdscript

# Positional Arguments:
srcfile=" input_csv/input-full-cori"$version" "
template=$CSCRATCH/bosslover/scaling-test/ost2/$SLURM_JOB_ID.h5
pmfquery=" pmf-list/large-scale/pmf1k-shuffle.csv "

# Optional Arguments:
k_opt1=" --mpi="         # 'yes' for parallel read/wirte 
                         # 'no'  for serial read/write

k_opt2=" --template="    # 'yes' for creating a template only 
 		         # 'no'  for using previous template and writing the actual data into it
		         # 'all' for creating a template and writing the actual data into it

k_opt3=" --fiber="       # specify a file that could store the accessed fiber information
k_opt4=" --catalog="     # specify a file that could store the accssed catalog information
k_opt5=" --datamap="     # specify a file that stored all fiber information of source files
                         # if not specified, will scan all source files to create a new datamap

v_opt1="yes "
v_opt2="all "
v_opt3=$SLURM_JOB_ID"_fiber.txt "
v_opt4=$SLURM_JOB_ID"_catalog.txt "
v_opt5="datamap1.pk"



run=$cmd$srcfile$template$pmfquery$k_opt1$v_opt1$k_opt2$v_opt2$k_opt3$v_opt3$k_opt4$v_opt4$k_opt5$v_opt5
echo $run
$run
