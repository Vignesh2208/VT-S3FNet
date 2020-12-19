NUM_CORES := 4


all: 
	echo "inc | rebuild | debuginc | debug"

inc: lxcman
	./build.sh -i -t -n $(NUM_CORES)

rebuild: lxcman
	./build.sh -f -t -n  $(NUM_CORES)
	
fullbuild: lxcman
	./build.sh -t -n $(NUM_CORES)

debuginc: lxcman
	./build.sh -i -t -f -d -n $(NUM_CORES)

debug: lxcman
	./build.sh -f -t -d -n $(NUM_CORES)

lxcman:
	cd tklxcmngr; make clean; make;

csudp:
	cd ../csudp; make;

mpi_test:
	sudo rm -f /tmp/endpoints > /dev/null
	cd s3fnet/test/lxc_tests/mpi_mm/; make clean; make; make test
	chmod -R 777 ../experiment-data	


small_2_tcp_large_pings:
	cd s3fnet/test/lxc_tests/small_2_tcp_large_pings/; make clean; make; make test
	chmod -R 777 ../experiment-data	

small_2_udp_large_pings:
	cd s3fnet/test/lxc_tests/small_2_udp_large_pings/; make clean; make; make test
	chmod -R 777 ../experiment-data	

examplerun:
	cd s3fnet/test/lxc_tests/large_emu_only_2/; make clean; make; make test
	chmod -R 777 ../experiment-data

run:	
	# cd s3fnet/test/lxc_tests/small_2_udp_tiny_delay/; make clean; make; make test
	# cd s3fnet/test/lxc_tests/small_2_udp_2_emu_1_router/; make clean; make; make test
	# cd s3fnet/test/lxc_tests/sandbox/; make clean; make; make test
	cd s3fnet/test/lxc_tests/small_2_udp/; make clean; make; make test
	# cd s3fnet/test/lxc_tests/small_2_udp_large_pings/; make clean; make; make test
	# cd s3fnet/test/lxc_tests/small_1_ping/; make clean; make; make test
	# cd s3fnet/test/lxc_tests/large/; make clean; make; make test
	# cd s3fnet/test/lxc_tests/large_emu_only_25/; make clean; make; make test
	# cd s3fnet/test/lxc_tests/large_emu_only_2/; make clean; make; make test
	# cd s3fnet/test/lxc_tests/huge_with_traffic/; make clean; make; make test
	chmod -R 777 ../experiment-data
	
	
