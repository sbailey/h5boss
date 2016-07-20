#!/bin/bash
#SBATCH -p regular
#SBATCH -N 1
#SBATCH -t 04:00:00
#SBATCH -J subset-serial-index
#SBATCH -e %j_10k_ind.err
#SBATCH -o %j_10k_ind.out
cd $SLURM_SUBMIT_DIR
TESTDIR=$SCRATCH/bosslover/scaling-test/
#rm -rf TESTDIR
#mkdir -p $TESTDIR || exit
#subset input-full $TESTDIR/pmf100-s.h5 pmf-list/pmf100

for i in `seq 1 1`;
do 
        echo $TESTDIR/id10k_$i.2.h5
	#subset_idx input-full1 $TESTDIR/id$i.h5 pmf-list/pmf1k1
        cmd="subset_idx input-full1 "$TESTDIR"/id10k_"$i".2.h5 pmf-list/pmf10k"
	echo $cmd
        $cmd
	#shuf input-full1 > input-full2
	#mv input-full2 input-full1
	#shuf pmf-list/pmf1k1 > pmf-list/pmf1k2
	#mv pmf-list/pmf1k2 pmf-list/pmf1k1
done
#subset_idx input-full1 /scratch1/scratchdirs/jialin/bosslover/scaling-test/id1.h5 pmf-list/pmf1k1
