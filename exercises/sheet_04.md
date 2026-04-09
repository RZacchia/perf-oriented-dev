Exercise Sheet 4
================

For this exercise, perform all measurments on LCC3. You can of course (and probably should) run analysis tools (e.g. massif-visualizer) locally.

A) Memory profiling
-------------------

In `larger_samples` you find two somewhat larger C programs. The first one you are already familiar with. The second one, "SSCA2", takes a "scale" as its command line parameter -- use `ssca2 17` for this exercise.

For both programs:
 * Use the valgrind "massif" tool in Valgrind to determine the largest sources of heap memory utilization, and visualize the results with "massif-visualizer".
 * How significant is the perturbation in execution time caused by using massif?

Summarize, interpret and report your findings.

B) Measuring CPU counters
-------------------------

For both programs, measure **all** events in the `[Hardware cache event]` category reported by `perf list`. Note that as discussed in the lecture, there is a limit on the number of hardware counters you can measure in a single run.

For both programs:
 * Report the results in **relative** metrics, and compare these between the programs.
 * How significant is the perturbation in execution time caused by using perf to measure performance counters?

Summarize, interpret and report your findings.


Submission
----------
Please submit your solutions by email to peter.thoman at UIBK, using the string "[Perf2026-sheet4]" in the subject line, before the start of the next VU at the latest.  
Try not to include attachments with a total size larger than 2 MiB.



lcc3 events

L1-dcache-load-misses                              [Hardware cache event]
L1-dcache-loads                                    [Hardware cache event]
L1-dcache-prefetch-misses                          [Hardware cache event]
L1-dcache-prefetches                               [Hardware cache event]
L1-dcache-store-misses                             [Hardware cache event]
L1-dcache-stores                                   [Hardware cache event]
L1-icache-load-misses                              [Hardware cache event]
L1-icache-loads                                    [Hardware cache event]
LLC-load-misses                                    [Hardware cache event]
LLC-loads                                          [Hardware cache event]
LLC-prefetch-misses                                [Hardware cache event]
LLC-prefetches                                     [Hardware cache event]
LLC-store-misses                                   [Hardware cache event]
LLC-stores                                         [Hardware cache event]
branch-load-misses                                 [Hardware cache event]
branch-loads                                       [Hardware cache event]
dTLB-load-misses                                   [Hardware cache event]
dTLB-loads                                         [Hardware cache event]
dTLB-store-misses                                  [Hardware cache event]
dTLB-stores                                        [Hardware cache event]
iTLB-load-misses                                   [Hardware cache event]
iTLB-loads                                         [Hardware cache event]
node-load-misses                                   [Hardware cache event]
node-loads                                         [Hardware cache event]
node-prefetch-misses                               [Hardware cache event]
node-prefetches                                    [Hardware cache event]
node-store-misses                                  [Hardware cache event]
node-stores                                        [Hardware cache event]
