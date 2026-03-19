#!/bin/bash

#SBATCH --partition=lva
#SBATCH --job-name ex03
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

./npb_bt_a
mv gmon.out gmon_a.out
gprof ./npb_bt_a gmon_a.out > ~/perf-oriented-dev/profile_a.txt

./npb_bt_b
mv gmon.out gmon_b.out
gprof ./npb_bt_b gmon_b.out > ~/perf-oriented-dev/profile_b.txt