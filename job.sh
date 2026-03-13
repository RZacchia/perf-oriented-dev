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

mkdir -p /tmp/cb761245/



mkdir -p ~/perf-oriented-dev/tools/build
cd ~/perf-oriented-dev/tools/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja

cd ~/perf-oriented-dev/

echo ========== Starting Running with external CPU load ================
python3 benchmark.py -c bench_config_lcc3.json -o lcc3_cpu.csv



echo ========== Starting Running with external I/O load ================
python3 benchmark.py -c io_bench_config_lcc3.json -o lcc3_io.csv


echo ========= Starting cleaning ================
rm -r ~/perf-oriented-dev/small_samples/build
rm -r ~/perf-oriented-dev/tools/build
rm -r /tmp/cb761245/
