# Exercise 2 - Robert Zacchia

## Task A

The loadgen program makes heavy calculations according to a predesigned profile. It starts the loadgen program multiple times in the background, and then starts your benchmark with a high nice value. The nice value determines how the operating system should prioritize the running program. A higher nice factor means a higher priorization.

The External cpu load had a high impact on the small_samples program In the table below, I have the percentage of the the standard deviation of the overall executions.



// insert tables with variations


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

The impact on the io benchmarks was even more severe since sometimes the executions just would not work, with any