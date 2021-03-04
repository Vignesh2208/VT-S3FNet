#!/bin/bash

# Runs all Map-Reduce style jobs presented in the paper.
# To run without lookahead: ./runMPIExperiments.sh 0
# To run with lookahead: ./runMPIExperiments.sh 1

ENABLE_LOOKAHEAD=$1
S3FNET_DIR=$HOME/VT-S3FNet/base
TEST_DIR=$S3FNET_DIR/s3fnet/test/lxc_tests/fat_tree
TITAN_DIR=$HOME/Titan


declare -a mpiType=("int" "sat" "mm")
declare -a NumEmuHosts=(21 41 61 81 101)


cd $TITAN_DIR
sudo make unload
sudo make load

for numEmu in ${NumEmuHosts[@]}; do
   for type in ${mpiType[@]}; do
      echo "Starting MPI experiment .... "
      echo "Num Emulated Hosts = " $numEmu
      echo "MPI-Type = " $type
      cd $TEST_DIR
      python network_gen.py --num_emu_hosts=$numEmu --mpi_type=$type --enable_lookahead=$ENABLE_LOOKAHEAD 
      cd $S3FNET_DIR
      sudo make fat_tree_run
      cd $TITAN_DIR
      sudo make unload
      sudo make load
      echo 'Waiting 10 seconds ....'
      sleep 10
   done 
done


