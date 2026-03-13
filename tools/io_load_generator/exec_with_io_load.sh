killall ioloadgen &> /dev/null 
./tools/build/ioloadgen 3 40 1024 1048576 /tmp/cb761245/load1/ 12345 &> /dev/null &
./tools/build/ioloadgen 3 40 1024 1048576 /tmp/cb761245/load2/ 54321 &> /dev/null &
./tools/build/ioloadgen 3 40 1024 1048576 /tmp/cb761245/load3/ 24135 &> /dev/null &
./tools/build/ioloadgen 3 40 1024 1048576 /tmp/cb761245/load4/ 13524 &> /dev/null &
./tools/build/ioloadgen 3 40 1024 1048576 /tmp/cb761245/load5/ 53142 &> /dev/null &
./tools/build/ioloadgen 3 40 1024 1048576 /tmp/cb761245/load6/ 42531 &> /dev/null &
#time -p nice -n 100 $1
echo "starting $*"
nice -n 1000 $@
killall ioloadgen &> /dev/null &