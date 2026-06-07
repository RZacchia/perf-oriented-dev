#!/bin/bash
LOG=../../abc.log
echo ========== Starting building ================

mkdir -p ~/Desktop/perf-oriented-dev/ex11/build
cd ~/Desktop/perf-oriented-dev/ex11/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja


run_timed () {
  # $1 = name, rest = command...
  local name="$1"; shift
  /usr/bin/time -o "$LOG" -a -f "${name},%e,%U,%S,%P,%M" "$@"

}

N=500



echo ========== Starting running ================
for i in {1..2}
    do
    echo "========== Run $i / 15 =========="
    #run_timed delannoy ./delannoy $N    
    run_timed delannoy_memoized ./delannoy_memoized $N
    run_timed delannoy_tabulated ./delannoy_tabulated $N
    done

# python3 ../../parse_bench_log.py ../../abc.log ../../abc.csv