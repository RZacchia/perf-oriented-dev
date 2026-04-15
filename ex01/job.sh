#!/bin/bash

#SBATCH --partition=lva
#SBATCH --job-name ex01
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

mkdir -p ~/perf-oriented-dev/small_samples/build
cd ~/perf-oriented-dev/small_samples/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja

LOG="../../${SLURM_JOB_ID}.log"

run_timed () {
  # $1 = name, rest = command...
  local name="$1"; shift
  /bin/time -o "$LOG" -a -f "${name},%e,%U,%S,%P,%M" "$@"
}




echo ========== Starting running ================
for i in {1..15}
    do
    echo "========== Run $i / 15 =========="
    run_timed delannoy ./delannoy 13    
    run_timed filegen ./filegen 3 40 1024 1048576
    run_timed mmul ./mmul
    run_timed nbody ./nbody
    run_timed qap ./qap ../qap/problems/chr15c.dat
    done

python3 ../parse_bench_log.py ../../${SLURM_JOB_ID}.log ../../results_O3.csv

echo ========= Starting cleaning ================
rm -rf ~/perf-oriented-dev/small_samples/build
