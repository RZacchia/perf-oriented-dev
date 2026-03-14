# Exercise 2 - Robert Zacchia

## Task A

The loadgen program makes heavy calculations according to a predesigned profile. It starts the loadgen program multiple times in the background, and then starts your benchmark with a high nice value. The nice value determines how the operating system should prioritize the running program. A higher nice factor means a higher priorization.

The External cpu load had a high impact on the small_samples program In the table below, I have the percentage of the the standard deviation of the overall executions.


### Average results Local
| benchmark | avg_wall_s | avg_user_s | avg_sys_s | avg_cpu_pct | avg_max_rss_kb |
|---|---|---|---|---|---|
| delannoy | 2.358000 | 2.357000 | 0.000000 | 99.100000 | 1388.400000 |
| delannoy_load | 2.406000 | 2.836000 | 0.011667 | 118.033333 | 2766.800000 |
| filegen | 0.345000 | 0.319000 | 0.017333 | 98.333333 | 2600.133333 |
| filesearch | 0.000000 | 0.000000 | 0.000000 | 52.500000 | 1507.466667 |
| filesearch_load | 0.000000 | 0.000000 | 0.000000 | 100.000000 | 2108.000000 |
| mmul | 0.700000 | 0.687000 | 0.008333 | 99.366667 | 24629.600000 |
| mmul_load | 0.731333 | 1.099667 | 0.022000 | 153.266667 | 24577.866667 |
| nbody | 0.442000 | 0.440000 | 0.000000 | 99.400000 | 1508.800000 |
| nbody_load | 0.475333 | 0.840333 | 0.010667 | 178.966667 | 2741.733333 |
| qap | 1.338000 | 1.336000 | 0.000000 | 99.500000 | 1618.000000 |
| qap_load | 1.370000 | 1.856667 | 0.011333 | 135.866667 | 2814.933333 |

---

### Variance results Local
| benchmark | runs | wall_s_var_pct | user_s_var_pct | sys_s_var_pct | cpu_pct_var_pct | max_rss_kb_var_pct |
|---|---|---|---|---|---|---|
| delannoy | 10 | 0.169635 | 0.194424 | 0.000000 | 0.302725 | 1.493966 |
| delannoy_load | 30 | 0.675315 | 3.002498 | 31.943828 | 2.701226 | 3.173146 |
| filegen | 30 | 4.718499 | 1.481447 | 25.512498 | 3.707179 | 2.261120 |
| filesearch | 30 | 0.000000 | 0.000000 | 0.000000 | 87.491626 | 1.056359 |
| filesearch_load | 10 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| mmul | 30 | 0.368856 | 0.852906 | 44.721360 | 0.484966 | 0.441566 |
| mmul_load | 30 | 0.682162 | 5.273716 | 18.181818 | 4.991573 | 0.464535 |
| nbody | 10 | 0.904977 | 0.000000 | 0.000000 | 0.492855 | 3.775022 |
| nbody_load | 30 | 1.300648 | 7.491566 | 23.385359 | 7.816675 | 0.882369 |
| qap | 10 | 0.298954 | 0.366690 | 0.000000 | 0.502513 | 3.001953 |
| qap_load | 30 | 1.206773 | 13.258987 | 37.665437 | 11.630808 | 4.046701 |

---


### Average results lcc3
| benchmark | avg_wall_s | avg_user_s | avg_sys_s | avg_cpu_pct | avg_max_rss_kb |
|---|---|---|---|---|---|
| delannoy | 12.375000 | 12.341000 | 0.000000 | 99.000000 | 1375.200000 |
| delannoy_load | 15.079333 | 14.360333 | 0.010333 | 94.966667 | 3193.866667 |
| filegen | 1.538667 | 0.772667 | 0.040667 | 53.400000 | 2479.466667 |
| filegen_load | 1.634333 | 0.886333 | 0.054333 | 57.533333 | 3199.333333 |
| filesearch | 0.000000 | 0.000000 | 0.000000 | 100.000000 | 1468.000000 |
| filesearch_load | 0.010000 | 0.000000 | 0.000000 | 81.633333 | 3194.000000 |
| mmul | 2.054000 | 2.037000 | 0.000000 | 99.000000 | 24560.800000 |
| mmul_load | 2.296000 | 2.183000 | 0.010000 | 95.400000 | 24552.800000 |
| nbody | 2.561000 | 2.554000 | 0.000000 | 99.000000 | 1888.800000 |
| nbody_load | 2.847000 | 2.731333 | 0.002667 | 95.633333 | 3173.200000 |
| qap | 3.109000 | 3.098000 | 0.000000 | 99.000000 | 1512.000000 |
| qap_load | 3.783000 | 3.606667 | 0.001667 | 95.033333 | 3197.866667 |

### Variance results lcc3_cpu
| benchmark | runs | wall_s_var_pct | user_s_var_pct | sys_s_var_pct | cpu_pct_var_pct | max_rss_kb_var_pct |
|---|---|---|---|---|---|---|
| delannoy | 10 | 0.245768 | 0.241602 | 0.000000 | 0.000000 | 2.813450 |
| delannoy_load | 30 | 1.031340 | 1.063633 | 39.375986 | 0.189019 | 1.258536 |
| filegen | 30 | 12.377660 | 3.823731 | 17.883135 | 9.809589 | 1.948734 |
| filegen_load | 30 | 5.490227 | 4.072979 | 11.328948 | 4.679680 | 1.316077 |
| filesearch | 10 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 3.077934 |
| filesearch_load | 30 | 0.000000 | 0.000000 | 0.000000 | 9.710099 | 1.938714 |
| mmul | 10 | 3.339129 | 3.264143 | 0.000000 | 0.000000 | 0.240440 |
| mmul_load | 10 | 3.523301 | 3.059584 | 0.000000 | 0.960708 | 0.247372 |
| nbody | 10 | 0.443491 | 0.501419 | 0.000000 | 0.000000 | 0.897485 |
| nbody_load | 30 | 0.851487 | 0.532522 | 165.831240 | 0.831430 | 1.812209 |
| qap | 10 | 0.267180 | 0.241553 | 0.000000 | 0.000000 | 4.241063 |
| qap_load | 30 | 1.897798 | 1.878226 | 223.606798 | 0.743235 | 1.741531 |



To improve my experimental setup, I changed the python script to include the following parameters starting parameters:

```bash
--config #path to JSON config file
--out #Output CSV file
--std_dev # % standard deviation that must be reached
--min_runs #minimum number of runs before std_dev check happens
--max_runs # fallback so that the program does not run indefinetelly
--warmups # benchmark runs that do not get meassured
```
I did all experimental runs on lcc3 and local with the following boundaries:
```bash
python3 benchmark.py --min-runs 10 --max-runs 30 --std-dev 5
```
I also made a configuration file, to adjust working directories etc, for each environment. In there the build steps, and the exectables with parameters and working directory during execution are defined.

```json
{
  
  "cwd": "small_samples/build", //global working directory
  "build": [
    "cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release",
    "ninja"
  ],
  "benchmarks": [
    {
      "name": "delannoy",
      "cmd": ["./delannoy", "14"]
    },
    {
      "name": "delannoy_load",
      "cmd": ["./tools/load_generator/exec_with_workstation_heavy.sh", "./small_samples/build/delannoy", "14"],
      "cwd": "/home/robert/Desktop/perf-oriented-dev/" // working directory for this execution
    },
    // etc...
  ]
}
```


The benchmark script itself stores the current perfomance values of each execution, calculates the standart deviation after each execution, and checks if a criterium for finishing has been met. If 1 of the finishing condition is met, it writes the csv with the raw formatted /bin/times values for each execution.

```csv
benchmark,run,wall_s,user_s,sys_s,cpu_pct,max_rss_kb
filegen,1,0.36,0.34,0.02,100.0,2588
filegen,2,0.35,0.33,0.02,100.0,2688
...
```
and another one with just the variances for each parameter for each run.
```csv
benchmark,runs,wall_s_var_pct,user_s_var_pct,sys_s_var_pct,cpu_pct_var_pct,max_rss_kb_var_pct
delannoy,40,0.4293266340877432,0.43770903419832846,0,0.4032258064516129,3.1144886324745413
delannoy_load,40,0.7349666174479198,4.062141332659616,31.049688819751527,3.4406509219377983,2.2532646825429126
```



## Task B
To create the I/O loadgenerator, I copied the filegen.c file and reworked it. The rework included Signal handlers and putting the main for loop of the original into a while loop that gets set to false, should the program register a SIGTERM or SIGINT signal, similar to the loadgen that we used in the previous task.

```c
while (run)
    {
        // original filegen loop
        for (int i = 0; i < num_directories; i++) {
            char dirname[MAX_FILENAME_LENGTH];
            snprintf(dirname, MAX_FILENAME_LENGTH, "dir_%d", i);
            create_files(parent_dir, dirname, num_files, min_file_size, max_file_size);
        }
    }
```

Similar to the exec_with_heavy_workstation.sh script file, I made this script file to execute the I/O benchmarks with I/O loads.


```bash
killall ioloadgen &> /dev/null 
./tools/build/ioloadgen 5 400 1024 1048576 /tmp/cb761245/load1/ 12345 &> /dev/null &
./tools/build/ioloadgen 2 1000 1024 2048 /tmp/cb761245/load2/ 54321 &> /dev/null &
./tools/build/ioloadgen 3 20 1048576 1048576 /tmp/cb761245/load3/ 24135 &> /dev/null &
./tools/build/ioloadgen 10 20 4096 1048576 /tmp/cb761245/load4/ 13524 &> /dev/null &
./tools/build/ioloadgen 1 200 1024 1048576 /tmp/cb761245/load5/ 53142 &> /dev/null &
./tools/build/ioloadgen 3 100 1024 1048576 /tmp/cb761245/load6/ 42531 &> /dev/null &
echo "starting $*"
nice -n 1000 $@
killall ioloadgen &> /dev/null &

rm -r /tmp/cb761245/load1/
rm -r /tmp/cb761245/load2/
rm -r /tmp/cb761245/load3/
rm -r /tmp/cb761245/load4/
rm -r /tmp/cb761245/load5/
rm -r /tmp/cb761245/load6/

```

## I/O load Results

### Average results local
| benchmark | avg_wall_s | avg_user_s | avg_sys_s | avg_cpu_pct | avg_max_rss_kb |
|---|---|---|---|---|---|
| filegen | 0.345000 | 0.322000 | 0.019667 | 99.233333 | 2608.133333 |
| filegen_load | 0.524000 | 0.726000 | 0.267000 | 189.800000 | 2734.400000 |
| filesearch | 0.000000 | 0.000000 | 0.000000 | 34.166667 | 1503.200000 |
| filesearch_load | 0.063667 | 0.003000 | 0.080000 | 131.366667 | 2739.866667 |

---

### Variance results local
| benchmark | runs | wall_s_var_pct | user_s_var_pct | sys_s_var_pct | cpu_pct_var_pct | max_rss_kb_var_pct |
|---|---|---|---|---|---|---|
| filegen | 30 | 1.944407 | 2.324011 | 20.689077 | 0.426220 | 2.423798 |
| filegen_load | 10 | 4.991106 | 2.902384 | 2.925187 | 3.941329 | 0.382583 |
| filesearch | 30 | 0.000000 | 0.000000 | 0.000000 | 131.562160 | 1.467812 |
| filesearch_load | 30 | 32.817663 | 230.136835 | 46.881944 | 19.641538 | 0.026206 |


### Average results lcc3
| benchmark | avg_wall_s | avg_user_s | avg_sys_s | avg_cpu_pct | avg_max_rss_kb |
|---|---|---|---|---|---|
| filegen | 1.479333 | 0.763000 | 0.042333 | 54.866667 | 2490.000000 |
| filegen_load | 6.826667 | 2.558000 | 0.385667 | 41.400000 | 3425.066667 |
| filesearch | 0.110333 | 0.000000 | 0.012667 | 17.100000 | 1467.066667 |
| filesearch_load | 0.094000 | 0.001333 | 0.056333 | 84.500000 | 3191.600000 |

### Variance results lcc3
| benchmark | runs | wall_s_var_pct | user_s_var_pct | sys_s_var_pct | cpu_pct_var_pct | max_rss_kb_var_pct |
|---|---|---|---|---|---|---|
| filegen | 30 | 10.184569 | 0.767951 | 9.991006 | 7.286350 | 1.885185 |
| filegen_load | 30 | 24.119898 | 117.434586 | 40.787560 | 97.996611 | 10.093762 |
| filesearch | 30 | 28.611723 | 0.000000 | 34.911840 | 11.729970 | 3.040769 |
| filesearch_load | 30 | 88.564495 | 254.950976 | 46.625567 | 24.398510 | 3.395830 |

---