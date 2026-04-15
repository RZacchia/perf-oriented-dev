#!/bin/bash

#SBATCH --partition=lva
#SBATCH --job-name ex05_a_o1
#SBATCH --output=%j_job_output.log
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --exclusive

module purge
module load gcc/12.2.0-gcc-8.5.0-p4pe45v
module load cmake/3.24.3-gcc-8.5.0-svdlhox
module load ninja/1.11.1-python-3.10.8-gcc-8.5.0-2oc4wj6
module load python/3.10.8-gcc-8.5.0-r5lf3ij
gcc -Q --help=optimizer -O3 | grep funroll
echo =============== Cleanup =================
rm -rf ~/perf-oriented-dev/small_samples/build
rm -rf ~/perf-oriented-dev/larger_samples/ssca2/build
rm -rf ~/perf-oriented-dev/larger_samples/npb_bt/build

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
LOG2="../../../${SLURM_JOB_ID}.log"

run_timed2 () {
  # $1 = name, rest = command...
  local name="$1"; shift
  /bin/time -o "$LOG2" -a -f "${name},%e,%U,%S,%P,%M" "$@"
}



echo ========== Starting running ================
for i in {1..15}
    do
    run_timed delannoy ./delannoy 13    
    done

for i in {1..15}
    do
    run_timed mmul ./mmul
    done

for i in {1..15}
    do
    run_timed nbody ./nbody
    done

for i in {1..15}
    do
    run_timed qap ./qap ../qap/problems/chr15c.dat
    done

echo ========== Starting building ================
mkdir -p ~/perf-oriented-dev/larger_samples/npb_bt/build
cd ~/perf-oriented-dev/larger_samples/npb_bt/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja

for i in {1..15}
    do
    run_timed2 npbbtw ./npb_bt_w
    done

echo ========== Starting building ================
mkdir -p ~/perf-oriented-dev/larger_samples/ssca2/build
cd ~/perf-oriented-dev/larger_samples/ssca2/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja

for i in {1..15}
    do
    run_timed2 scca2 ./ssca2 15
    done

python3 ~/perf-oriented-dev/parse_bench_log.py ~/perf-oriented-dev/${SLURM_JOB_ID}.log ~/perf-oriented-dev/results_fversion_loops_for_strides.csv

echo =============== Cleanup =================
rm -rf ~/perf-oriented-dev/small_samples/build
rm -rf ~/perf-oriented-dev/larger_samples/ssca2/build
rm -rf ~/perf-oriented-dev/larger_samples/npb_bt/build

