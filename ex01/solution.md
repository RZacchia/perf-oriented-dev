# Perfomance Oriented Programming EX01 -- Zacchia Robert

```bash
#!/bin/bash

#SBATCH --partition=lva
#SBATCH --job-name ex01
#SBATCH --output=%j_output.log
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --exclusive

module purge
module load gcc/12.2.0-gcc-8.5.0-p4pe45v 
module load cmake/3.24.3-gcc-8.5.0-svdlhox 
module load ninja/1.11.1-python-3.10.8-gcc-8.5.0-2oc4wj6
module load python/3.10.8-gcc-8.5.0-r5lf3ij

echo ========== Starting building ================

mkdir -p ~/perf-oriented-dev/small_samples/build
cd ~/perf-oriented-dev/small_samples/build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja


echo ========== Starting running ================
for i in {1..3}
    do
    echo "Run $i / 15"
    echo ============ Delannoy ================
    time  ./delannoy 13
    echo ============ Filegen ================
    time  ./filegen
    echo ============ mmul ================
    time  ./mmul
    echo ============ nbody ================
    time  ./nbody
    echo ============ qap ================
    time  ./qap ../qap/problems/chr18b.dat
    done


echo ========= Starting cleaning ================
rm -rf ~/perf-oriented-dev/small_samples/build
echo ========= Done ================


```


```bash
sbatch job.sh

# after job is completed
python3 ../parse_bench_log.py ../${SLURM_JOB_ID}_output.log ../results_${SLURM_JOB_ID}.csv
```