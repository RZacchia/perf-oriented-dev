#!/bin/bash
echo ========== Starting building ================

mkdir -p ~/perf-oriented-dev/ex11/build
cd ~/perf-oriented-dev/ex11/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja


run_timed () {
  # $1 = name, rest = command...
  local name="$1"; shift
  timed-run -o "$LOG" -a -f "${name},%e,%U,%S,%P,%M" "$@"
}




echo ========== Starting running ================
for i in {1..15}
    do
    echo "========== Run $i / 15 =========="
    run_timed delannoy ./delannoy 13    
    run_timed delannoy_memoized ./delannoy_memoized 13
    done

python3 ../parse_bench_log.py ../../abc.log ../../abc.csv