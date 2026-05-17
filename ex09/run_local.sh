#!/bin/bash


make

./build/container_benchmark 100 8 10 > local.log
./build/container_benchmark 99 8 10 >> local.log
./build/container_benchmark 10 8 10 >> local.log
./build/container_benchmark 50 8 10 >> local.log

./build/container_benchmark 100 8 1000 >> local.log
./build/container_benchmark 99 8 1000 >> local.log
./build/container_benchmark 10 8 1000 >> local.log
./build/container_benchmark 50 8 1000 >> local.log

./build/container_benchmark 100 8 100000 >> local.log
./build/container_benchmark 99 8 100000 >> local.log
./build/container_benchmark 10 8 100000 >> local.log
./build/container_benchmark 50 8 100000 >> local.log

./build/container_benchmark 100 8 10000000 >> local.log
./build/container_benchmark 99 8 10000000 >> local.log
./build/container_benchmark 10 8 10000000 >> local.log
./build/container_benchmark 50 8 10000000 >> local.log



./build/container_benchmark 100 512 10 >> local.log
./build/container_benchmark 99 512 10 >> local.log
./build/container_benchmark 10 512 10 >> local.log
./build/container_benchmark 50 512 10 >> local.log

./build/container_benchmark 100 512 1000 >> local.log
./build/container_benchmark 99 512 1000 >> local.log
./build/container_benchmark 10 512 1000 >> local.log
./build/container_benchmark 50 512 1000 >> local.log

./build/container_benchmark 100 512 100000 >> local.log
./build/container_benchmark 99 512 100000 >> local.log
./build/container_benchmark 10 512 100000 >> local.log
./build/container_benchmark 50 512 100000 >> local.log

./build/container_benchmark 100 512 10000000 >> local.log
./build/container_benchmark 99 512 10000000 >> local.log
./build/container_benchmark 10 512 10000000 >> local.log
./build/container_benchmark 50 512 10000000 >> local.log


./build/container_benchmark 100 8388608 10 >> local.log
./build/container_benchmark 99 8388608 10 >> local.log
./build/container_benchmark 10 8388608 10 >> local.log
./build/container_benchmark 50 8388608 10 >> local.log

./build/container_benchmark 100 8388608 1000 >> local.log
./build/container_benchmark 99 8388608 1000 >> local.log
./build/container_benchmark 10 8388608 1000 >> local.log
./build/container_benchmark 50 8388608 1000 >> local.log

make clean