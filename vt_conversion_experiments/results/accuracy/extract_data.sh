#!/bin/bash
declare -a StringArray=("Sandy_Bridge" "Skylake")
declare -a Cmds=("sysbench" "bzip2" "sjeng" "h264ref")
declare -a Configs=("c1" "c2" "c3")

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# Iterate the string array using for loop
for arch in ${StringArray[@]}; do
   for cmd in ${Cmds[@]}; do
	for config in ${Configs[@]}; do
	   SubDir=$DIR/ins-counting/$arch/vt_${cmd}_${config}_ts1000000
	   echo 'Processing: ' $SubDir 
	   if [ $cmd = "sysbench" ]; then
   		grep -nr "total time:" $SubDir/* | awk '{print $4'} | sed 's/s$//' > $SubDir/val.txt
	   else
  		grep -nr "Time taken:" $SubDir/* | awk '{print $3'} > $SubDir/val.txt
	   fi
	   SubDir=$DIR/normal/$arch/normal_${cmd}_${config}
	   echo 'Processing: ' $SubDir 
	   if [ $cmd = "sysbench" ]; then
   		grep -nr "total time:" $SubDir/* | awk '{print $4'} | sed 's/s$//' > $SubDir/val.txt
	   else
  		grep -nr "Time taken:" $SubDir/* | awk '{print $3'} > $SubDir/val.txt
	   fi
	   SubDir=$DIR/PModel/$arch/vt_${cmd}_${config}_ts1000000
	   echo 'Processing: ' $SubDir 
	   if [ $cmd = "sysbench" ]; then
   		grep -nr "total time:" $SubDir/* | awk '{print $4'} | sed 's/s$//' > $SubDir/val.txt
	   else
  		grep -nr "Time taken:" $SubDir/* | awk '{print $3'} > $SubDir/val.txt
	   fi
	done
   done
done
