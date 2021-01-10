#!/bin/bash

ENABLE_LOOKAHEAD=$1
S3FNET_DIR=$HOME/VT-S3FNet/base
TEST_DIR=$S3FNET_DIR/s3fnet/test/lxc_tests/campus_network
TITAN_DIR=$HOME/Titan

#declare -a Periods=(200000 400000 600000 800000 1000000)
#declare -a MuArrivals=(200000 400000 600000 800000 1000000)

declare -a Periods=(200000)
declare -a MuArrivals=(200000)
declare -a Rates=(1 10 100 1000)
declare -a TxSizes=(8 256 2000)
declare -a NumEmuHostsPerLan=(5)


cd $TITAN_DIR
sudo make unload
sudo make load

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

