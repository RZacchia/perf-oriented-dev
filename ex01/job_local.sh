#!/bin/bash

SLURM_JOB_ID="1234665"

mkdir -p ~/Desktop/perf-oriented-dev/small_samples/build
cd ~/Desktop/perf-oriented-dev/small_samples/build
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

python3 ../parse_bench_log.py ../../${SLURM_JOB_ID}.log ../../${SLURM_JOB_ID}_results.csv

echo ========= Starting cleaning ================
rm -rf ~/Desktop/perf-oriented-dev/small_samples/build
