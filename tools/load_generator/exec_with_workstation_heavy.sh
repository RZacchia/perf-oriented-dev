killall loadgen &> /dev/null 
./tools/build/loadgen mc3 tools/load_generator/workstation/sys_load_profile_workstation_excerpt.txt &> /dev/null &
./tools/build/loadgen mc3 tools/load_generator/workstation/sys_load_profile_workstation_excerpt.txt &> /dev/null &
./tools/build/loadgen mc3 tools/load_generator/workstation/sys_load_profile_workstation_excerpt.txt &> /dev/null &
./tools/build/loadgen mc3 tools/load_generator/workstation/sys_load_profile_workstation_excerpt.txt &> /dev/null &
./tools/build/loadgen mc3 tools/load_generator/workstation/sys_load_profile_workstation_excerpt.txt &> /dev/null &
./tools/build/loadgen mc3 tools/load_generator/workstation/sys_load_profile_workstation_excerpt.txt &> /dev/null &
#time -p nice -n 100 $1
echo "starting $*"
nice -n 1000 $@
killall loadgen &> /dev/null &
