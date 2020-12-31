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

clean:
	cd tklxcmngr; make clean;
	cd s3fnet; make clean;
	cd api; make clean;
	cd aux; make clean;
	cd dml; make clean;
	cd metis; rm -f *.o *.a > /dev/null;
	cd rng; make clean;
	cd ../csudp; make clean;

csudp:
	cd ../csudp; make;

mpi_run:
	sudo rm -f /tmp/endpoints > /dev/null
	cd s3fnet/test/lxc_tests/mpi_mm/; make clean; make; make test
	chmod -R 777 ../experiment-data

fat_tree_run:
	cd s3fnet/test/lxc_tests/fat_tree/; make clean; make; make test
	chmod -R 777 ../experiment-data

campus_run:
	cd s3fnet/test/lxc_tests/campus_network/; make clean; make; make test
	chmod -R 777 ../experiment-data

small_2_tcp_large_pings:
	cd s3fnet/test/lxc_tests/small_2_tcp_large_pings/; make clean; make; make test
	chmod -R 777 ../experiment-data	


	
	
