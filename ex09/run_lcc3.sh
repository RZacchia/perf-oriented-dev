#!/bin/bash

#SBATCH --partition=lva
#SBATCH --job-name ex05_a_o1
#SBATCH --output=%j_job_output.log
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --exclusive

module purge
module load gcc/12.2.0-gcc-8.5.0-p4pe45v



make

./container_benchmark 100 8 10 > lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 8 10 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 8 10 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 8 10 >> lcc3_${SLURM_JOB_ID}.log

./container_benchmark 100 8 1000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 8 1000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 8 1000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 8 1000 >> lcc3_${SLURM_JOB_ID}.log

./container_benchmark 100 8 100000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 8 100000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 8 100000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 8 100000 >> lcc3_${SLURM_JOB_ID}.log

./container_benchmark 100 8 10000000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 8 10000000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 8 10000000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 8 10000000 >> lcc3_${SLURM_JOB_ID}.log



./container_benchmark 100 512 10 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 512 10 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 512 10 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 512 10 >> lcc3_${SLURM_JOB_ID}.log

./container_benchmark 100 512 1000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 512 1000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 512 1000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 512 1000 >> lcc3_${SLURM_JOB_ID}.log

./container_benchmark 100 512 100000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 512 100000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 512 100000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 512 100000 >> lcc3_${SLURM_JOB_ID}.log

./container_benchmark 100 512 10000000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 512 10000000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 512 10000000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 512 10000000 >> lcc3_${SLURM_JOB_ID}.log


./container_benchmark 100 8388608 10 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 8388608 10 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 8388608 10 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 8388608 10 >> lcc3_${SLURM_JOB_ID}.log

./container_benchmark 100 8388608 1000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 99 8388608 1000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 10 8388608 1000 >> lcc3_${SLURM_JOB_ID}.log
./container_benchmark 50 8388608 1000 >> lcc3_${SLURM_JOB_ID}.log

make clean