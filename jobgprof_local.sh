#!/bin/bash


mkdir -p ~/Desktop/perf-oriented-dev/larger_samples/npb_bt/build
cd ~/Desktop/perf-oriented-dev/larger_samples/npb_bt/
cd build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja

./npb_bt_a
mv gmon.out gmon_a.out
gprof ./npb_bt_a gmon_a.out > profile_a_local_1.txt

./npb_bt_a
mv gmon.out gmon_a.out
gprof ./npb_bt_a gmon_a.out > profile_a_local_2.txt

./npb_bt_a
mv gmon.out gmon_a.out
gprof ./npb_bt_a gmon_a.out > profile_a_local_3.txt

./npb_bt_a
mv gmon.out gmon_a.out
gprof ./npb_bt_a gmon_a.out > profile_a_local_4.txt

./npb_bt_b
mv gmon.out gmon_b.out
gprof ./npb_bt_b gmon_b.out > profile_b_local_1.txt

./npb_bt_b
mv gmon.out gmon_b.out
gprof ./npb_bt_b gmon_b.out > profile_b_local_2.txt

./npb_bt_b
mv gmon.out gmon_b.out
gprof ./npb_bt_b gmon_b.out > profile_b_local_3.txt

./npb_bt_b
mv gmon.out gmon_b.out
gprof ./npb_bt_b gmon_b.out > profile_b_local_4.txt