#!/bin/bash
#SBATCH -p regular
#SBATCH -N 1
#SBATCH -t 30:00:00
#SBATCH -J subset-serial
#SBATCH -e %j_100k.err
#SBATCH -o %j_100k.out
cd $SLURM_SUBMIT_DIR
TESTDIR=$SCRATCH/bosslover/scaling-test/
#rm -rf TESTDIR
#mkdir -p $TESTDIR || exit
#subset input-full $TESTDIR/pmf100-s.h5 pmf-list/pmf100

#for i in `seq 1 1`;
#do 
echo $TESTDIR/100k_$i.h5
	#subset_idx input-full1 $TESTDIR/100k_$i.h5 pmf-list/pmf100k
#        cmd="subset input-full "$TESTDIR"/100k_"$i".h5 pmf-list/pmf100k"
#	echo $cmd
        $cmd
	#shuf input-full1 > input-full2
	#mv input-full2 input-full1
	#shuf pmf-list/pmf1k1 > pmf-list/pmf1k2
	#mv pmf-list/pmf1k2 pmf-list/pmf1k1
#done
echo "subset input-full /scratch1/scratchdirs/jialin/bosslover/scaling-test/100k.1.h5 pmf-list/pmf100k"
subset input-full /scratch1/scratchdirs/jialin/bosslover/scaling-test/ost24/100k.1.h5 pmf-list/pmf100k
