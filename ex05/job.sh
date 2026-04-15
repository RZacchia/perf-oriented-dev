#!/bin/bash

#SBATCH --partition=lva
#SBATCH --job-name ex05
#SBATCH --output=%j_job_output.log
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --exclusive

module purge # clear all loaded modules
module load gcc/12.2.0-gcc-8.5.0-p4pe45v # a newer version of gcc
module load cmake/3.24.3-gcc-8.5.0-svdlhox # a newer version of cmake
module load ninja/1.11.1-python-3.10.8-gcc-8.5.0-2oc4wj6 # the ninja build system
module load python/3.10.8-gcc-8.5.0-r5lf3ij # a newer version of python

echo ========== Starting building ================
mkdir -p ~/perf-oriented-dev/larger_samples/npb_bt/build
cd ~/perf-oriented-dev/larger_samples/npb_bt/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja



PROGRAM="./npb_bt_a"

echo ========== Starting performance measurements ================
# echo l1-dcache-loads,l1-dcache-load-misses,l1-dcache-stores,l1-dcache-store-misses
# perf stat -r 3 -e L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,L1-dcache-store-misses $PROGRAM
# echo l1-icache-loads,l1-icache-load-misses
# perf stat -r 3 -e L1-dcache-prefetches,L1-dcache-prefetch-misses,L1-icache-loads,L1-icache-load-misses $PROGRAM
# perf stat -r 3 -e LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses $PROGRAM
# perf stat -r 3 -e LLC-prefetches,LLC-prefetch-misses $PROGRAM
# perf stat -r 3 -e dTLB-loads,dTLB-load-misses,dTLB-stores,dTLB-store-misses $PROGRAM
# perf stat -r 3 -e iTLB-loads,iTLB-load-misses $PROGRAM
# perf stat -r 3 -e node-loads,node-load-misses,node-stores,node-store-misses $PROGRAM
# perf stat -r 3 -e node-prefetches,node-prefetch-misses $PROGRAM
perf stat -r 3 -e branch-loads,branch-load-misses $PROGRAM

