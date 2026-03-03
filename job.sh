#!/bin/bash

#SBATCH --partition=lva
#SBATCH --job-name ex01
#SBATCH --output=%j_output.log
#SBATCH --ntasks=1
#SBATCH --exclusive

module purge # clear all loaded modules
module load gcc/12.2.0-gcc-8.5.0-p4pe45v # a newer version of gcc
module load cmake/3.24.3-gcc-8.5.0-svdlhox # a newer version of cmake
module load ninja/1.11.1-python-3.10.8-gcc-8.5.0-2oc4wj6 # the ninja build system
module load python/3.10.8-gcc-8.5.0-r5lf3ij # a newer version of python

mkdir -p small_samples/build
cd small_samples/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja

cd small_samples/build
/bin/time  ./mmul

python3 run_and_csv.py --build --runs 1 --output mmul_results.csv