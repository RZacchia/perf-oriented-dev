#!/bin/bash

make clean
make

./cache 512
./cache 1024
./cache 2048
./cache 4096
./cache 8192
./cache 16384
./cache 32768
./cache 65536
./cache 131072
./cache 262144
./cache 524288
./cache 1048576
./cache 2097152
./cache 4194304
./cache 8388608
./cache 16777216
./cache 33554432
./cache 67108864