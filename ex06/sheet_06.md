Exercise Sheet 6 - Robert Zacchia
================

A) MMUL tiling
--------------

Take the "mmul" small sample program and apply a tiling optimization to its main computation loop nest.
Think about which loop(s) to tile in order to achieve a meaningful performance benefit, and argue why your choice makes sense in terms of reuse distance reduction.

Test various tiling options on LCC3 (either manually or in an automated fashion) and report the results. Attempt to provide an explanation for the best parameter choices you found.

Note: use a **2048²** matrix for this benchmark.


B) Cache investigation
----------------------

Think about (and/or research) how you would implement a benchmark to measure cache latencies over progressively larger memory blocks, as seen in the lecture on memory optimization. Precisely explain its working principle and how it determines access latency while avoiding unintended effects.

## First Idea

1. Make x Bytes Array that fit into cache
2. Fill the array with arbitrary values
2. start clock
2. loop through the array, y amount of times, increment array value
2. end clock
3. calculate average time per access

C) Cache benchmark (optional)
-----------------------------

Implement your idea from B). Use the resulting program to measure and plot the access latency on LCC3 compute nodes for blocks of size 512 Byte to 16 MiB, in powers of 2.

## First try

To implement such fine grained timings, I tried to find a detailed, low overhead clock and found [clock_gettime()](https://man7.org/linux/man-pages/man3/clock_gettime.3.html). For all the measurements I implemented I did use this timing function with the Parameter CLOCK_MONOTONIC_RAW

```c
    sec0 = get_seconds();
    for ((int it = 0); it < iters; it++) {
        for (index = 0; index < limit; ++index) 
            array[index] = array[index] + 1;
    }
    sec = (get_seconds() - sec0);
```
L1 cache access on average was 0.06 ns. This was way faster than expected. So I suspected the structure of the program was to predictable to get specific measurements.
To prevent the outer loop from being optimized, I moved the time measurements into the outer loop. This way the compiler cannot apply optimizations to the same extend.


```c
    for (int it = 0; it < iters; it++) {
        sec0 = get_seconds();
        for (index = 0; index < limit; ++index) 
            array[index] = array[index] + 1;
        sec = sec + (get_seconds() - sec0);
    }
```

With the above version, I did get L1 cache hit access times of 0.55ns on my local machine. This still seemed low. I suspected some kind of vectorization and I then decided to disable all optimizations options. This way there was no meaningful difference execution times (1.05ns) between of the two versions.
I decided to move forward with the former. I added implementation details, to make the benchmark run configurable with command line arguments. 

After that I ran into a different problem. My timer did return acceptable values for L1 but with greater size the time that got returned fluctuated a lot.
My next attempt was to only meassure each array access directly and then calculate the mean

## Local measurements

### local cpu info

2 HT, 6 cores
L1d 192 KiB (x6)
L1i 192 KiB (x6)
L2    3 MiB (x6)
L3   16 MiB (x1)

### LCC3 Cpu Info




