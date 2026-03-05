# Perfomance Oriented Programming EX01 -- Zacchia Robert


### Preperations
The programs in the small folder directory contain different typical benchmarking examples.


| Program    |  Summary |
|------------|----------|
| delannoy   | delannoy is a recursive computational benchmark |
| filegen    | filegen creates directories, subdirectories and files with different filesizes |
| filesearch | recursive search of the largest file in a directory |
| mmul       | naive matrix multiplication  |
| nbody      | gravitational caculation between N bodies   |
| qap        | classic combinatorical optimisation problem |


Since the <lcc3_helper/modules.sh> file loads the module for ninja I build the programs as follows.

```bash
mkdir -p ~/perf-oriented-dev/small_samples/build
cd ~/perf-oriented-dev/small_samples/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja
```
I then chose the parameters by trying running the programs repeatetly until each programs execution time was around two seconds. In the end the parameter where as follows.

```bash
./delannoy 13    
./filegen 3 40 1024 1048576
./mmul
./nbody
./qap ../qap/problems/chr15c.dat
```

To automate the execution and csv generation I split the task in to different parts.
First my job sh script used /bin/time with the format "${name},%e,%U,%S,%P,%M" to get the statistics and write it into a seperate log file. I used to format the data from /bin/time so that the python script which generates the csv file was simpler. At the end of all execution rounds, a python script takes the log file and converts it to a csv with the following columns "program,avg_wall,var_wall,pct_std_wall,avg_cpu_pct,avg_peak_mem_kb". For this python script I used chatGPT to save on time.

### Results

Each run consists of calling each program once. For these results I made 15 runs. Instead of doing 15 times the same program before going to the next, I made the loop so that in each run each program is executed once.

lcc3 

| program   | avg_wall | var_wall  | pct_std_wall | avg_cpu_pct | avg_peak_mem_kb |
|-----------|----------|-----------|--------------|-------------|-----------------|
| delannoy  | 3.362667 | 0.000113  | 0.315967     | 99.00       | 1359.20         |
| filegen   | 1.620667 | 0.000646  | 1.568546     | 51.60       | 2506.40         |
| mmul      | 1.996667 | 0.001702  | 2.066344     | 99.00       | 24583.73        |
| nbody     | 2.555333 | 0.000038  | 0.241942     | 99.00       | 1874.13         |
| qap       | 3.222000 | 0.000083  | 0.282189     | 99.00       | 1516.80         |


local
Hardware:
AMD Ryzen 5 5600G 6 x 3,5GHz
32GB DDR4 RAM 2666 MHz

| program   | avg_wall | var_wall  | pct_std_wall | avg_cpu_pct | avg_peak_mem_kb |
|-----------|----------|-----------|--------------|-------------|-----------------|
| delannoy  | 0.401333 | 0.000078  | 2.203737     | 99.33       | 1298.13         |
| filegen   | 0.334000 | 0.000064  | 2.395210     | 99.27       | 2664.27         |
| mmul      | 0.714667 | 0.000065  | 1.127150     | 99.33       | 24484.53        |
| nbody     | 0.445333 | 0.000025  | 1.120257     | 99.27       | 1440.27         |
| qap       | 1.344667 | 0.000078  | 0.657734     | 99.13       | 1561.87         |

The results show the following:
- single core performance is slower on lcc3 
- Variance is higher on my home desktop
- Filegen does not seem to be IO bound on my home computer. This can be explained since the cluster uses network drives and my home computer has an M.2 NVME drive.
