# -- an example to run SPEC 429.mcf on gem5, put it under 429.mcf folder --
#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export GEM5_DIR=/home/titan/gem5
export BENCHMARK=$DIR/mmultiply_gcc



mkdir -p 2-way
time $GEM5_DIR/build/X86/gem5.opt -d $DIR/2-way $GEM5_DIR/configs/example/se.py -c $BENCHMARK -I 1000000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=128kB --l1i_size=128kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64


mkdir -p 8-way

time $GEM5_DIR/build/X86/gem5.opt -d $DIR/8-way $GEM5_DIR/configs/example/se.py -c $BENCHMARK -I 1000000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=128kB --l1i_size=128kB --l1d_assoc=8 --l1i_assoc=8 --cacheline_size=64
