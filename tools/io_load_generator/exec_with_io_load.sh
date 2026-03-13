killall ioloadgen &> /dev/null 
./tools/build/ioloadgen 5 400 1024 1048576 /tmp/cb761245/load1/ 12345 &> /dev/null &
./tools/build/ioloadgen 2 1000 1024 2048 /tmp/cb761245/load2/ 54321 &> /dev/null &
./tools/build/ioloadgen 3 20 1048576 1048576 /tmp/cb761245/load3/ 24135 &> /dev/null &
./tools/build/ioloadgen 10 20 4096 1048576 /tmp/cb761245/load4/ 13524 &> /dev/null &
./tools/build/ioloadgen 1 200 1024 1048576 /tmp/cb761245/load5/ 53142 &> /dev/null &
./tools/build/ioloadgen 3 100 1024 1048576 /tmp/cb761245/load6/ 42531 &> /dev/null &
#time -p nice -n 100 $1
echo "starting $*"
nice -n 1000 $@
killall ioloadgen &> /dev/null &

rm -r /tmp/cb761245/load1/
rm -r /tmp/cb761245/load2/
rm -r /tmp/cb761245/load3/
rm -r /tmp/cb761245/load4/
rm -r /tmp/cb761245/load5/
rm -r /tmp/cb761245/load6/
