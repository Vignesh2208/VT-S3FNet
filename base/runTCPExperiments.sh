#!/bin/bash

# Runs all TCP experiments presented in the paper.
# Note that running all experiments will take a while.
# You might want to selectively comment out and run some of them.


# To run without lookahead: ./runTCPExperiments.sh 0
# To run with lookahead: ./runTCPExperiments.sh 1

ENABLE_LOOKAHEAD=$1
S3FNET_DIR=$HOME/VT-S3FNet/base
TEST_DIR=$S3FNET_DIR/s3fnet/test/lxc_tests/campus_network
INCAST_TEST_DIR=$S3FNET_DIR/s3fnet/test/lxc_tests/fat_tree
TITAN_DIR=$HOME/Titan

# List of flow inter-arrival periods in us. Change as necessary
declare -a Periods=(200000 400000 600000 800000 1000000)

# List of mean flow inter-arrival times in us. Change as necessary
declare -a MuArrivals=(200000 400000 600000 800000 1000000)

# List of rates in Mbps. Change as necessary
declare -a Rates=(1 10 100 1000)

# List of burst transfer sizes in Kb. Change as necessary
declare -a TxSizes=(8 256 2000)

# Number of emulated hosts per lan. There are 20 lans.
declare -a NumEmuHostsPerLan=(1 2 3 4 5)

# Total number of incast flows + 1.
declare -a IncastSizes=(3 5 7 9 11)




cd $TITAN_DIR
sudo make unload
sudo make load

# Incast with Lookahead
for numEmu in ${IncastSizes[@]}; do
   for txSize in ${TxSizes[@]}; do
      echo "Starting TCP Incast experiment with Lookahead .... "
      echo "TxSize (kb) = " $txSize
      cd $INCAST_TEST_DIR
      python network_gen_incast.py --exp_type="incast_tgen" --incast_bsize_kb=$txSize --num_emu_hosts=$numEmu --incast_period_us=200000 --enable_lookahead=1 
      cd $S3FNET_DIR
      sudo make fat_tree_run
      cd $TITAN_DIR
      sudo make unload
      sudo make load
      echo 'Waiting 10 seconds ....'
      sleep 10
   done 
done

# Incast without Lookahead
for numEmu in ${IncastSizes[@]}; do
   for txSize in ${TxSizes[@]}; do
      echo "Starting TCP Incast experiment without Lookahead.... "
      echo "TxSize (kb) = " $txSize
      cd $INCAST_TEST_DIR
      python network_gen_incast.py --exp_type="incast_tgen" --incast_bsize_kb=$txSize --num_emu_hosts=$numEmu --incast_period_us=200000 --enable_lookahead=0 --run_time=5
      cd $S3FNET_DIR
      sudo make fat_tree_run
      cd $TITAN_DIR
      sudo make unload
      sudo make load
      echo 'Waiting 10 seconds ....'
      sleep 10
   done    
done

# Fixed inter-arrival times (Periodic bursty)
for numEmuPerLan in ${NumEmuHostsPerLan[@]}; do
   for period in ${Periods[@]}; do
      for txSize in ${TxSizes[@]}; do
         echo "Starting TCP Periodic experiment .... "
         echo "Num Emulated Hosts Per LAN = " $numEmuPerLan
         echo "Period (us) = " $period
         echo "TxSize (kb) = " $txSize
         cd $TEST_DIR
         python network_gen.py --num_emu_hosts_per_lan=$numEmuPerLan --emu_flow_type=periodic --emu_flow_period_us=$period --transfer_size_kb=$txSize --enable_lookahead=$ENABLE_LOOKAHEAD 
         cd $S3FNET_DIR
         sudo make campus_run
         cd $TITAN_DIR
         sudo make unload
         sudo make load
         echo 'Waiting 10 seconds ....'
         sleep 10
      done 
   done
done

# Exponential inter-arrival times (Poisson bursty)
for numEmuPerLan in ${NumEmuHostsPerLan[@]}; do
   for mu in ${MuArrivals[@]}; do
      for txSize in ${TxSizes[@]}; do
         echo "Starting TCP Poisson experiment .... "
         echo "Num Emulated Hosts Per LAN = " $numEmuPerLan
         echo "MuArrivals (us) = " $mu
         echo "TxSize (kb) = " $txSize
         cd $TEST_DIR
         python network_gen.py --num_emu_hosts_per_lan=$numEmuPerLan --emu_flow_type=poisson --emu_flow_mean_arrival_us=$mu --transfer_size_kb=$txSize --enable_lookahead=$ENABLE_LOOKAHEAD
         cd $S3FNET_DIR 
         sudo make campus_run
         cd $TITAN_DIR
         sudo make unload
         sudo make load
         echo 'Waiting 10 seconds ....'
         sleep 10
      done 
   done
done

# Constant Rate limited traffic pattern
for numEmuPerLan in ${NumEmuHostsPerLan[@]}; do
   for rate in ${Rates[@]}; do
      echo "Starting TCP Rate experiment .... "
      echo "Num Emulated Hosts Per LAN = " $numEmuPerLan
      echo "Rate (mbps) = " $rate
      cd $TEST_DIR
      python network_gen.py --num_emu_hosts_per_lan=$numEmuPerLan --emu_flow_type=rate --transfer_rate_mbps=$rate --enable_lookahead=$ENABLE_LOOKAHEAD 
      cd $S3FNET_DIR
      sudo make campus_run
      cd $TITAN_DIR
      sudo make unload
      sudo make load
      echo 'Waiting 10 seconds ....'
      sleep 10
   done
done

# Mixed Traffic
for numEmuPerLan in ${NumEmuHostsPerLan[@]}; do
   echo "Starting TCP Mixed experiment .... "
   echo "Num Emulated Hosts Per LAN = " $numEmuPerLan
   cd $TEST_DIR
   python network_gen.py --num_emu_hosts_per_lan=$numEmuPerLan --emu_flow_type=mixed --enable_lookahead=$ENABLE_LOOKAHEAD 
   cd $S3FNET_DIR
   sudo make campus_run
   cd $TITAN_DIR
   sudo make unload
   sudo make load
   echo 'Waiting 10 seconds ....'
   sleep 10
done

