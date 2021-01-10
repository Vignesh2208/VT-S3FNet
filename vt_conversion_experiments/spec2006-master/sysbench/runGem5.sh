# -- an example to run SPEC 429.mcf on gem5, put it under 429.mcf folder --
#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export GEM5_DIR=/home/titan/gem5
export BENCHMARK=/usr/local/bin/sysbench



mkdir -p 2-way
time $GEM5_DIR/build/X86/gem5.opt -d $DIR/2-way $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '--test=cpu --cpu-max-prime=5000 run' -I 1000000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64 --num-cpus=2


mkdir -p 8-way
time $GEM5_DIR/build/X86/gem5.opt -d $DIR/8-way $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '--test=cpu --cpu-max-prime=5000 run' -I 1000000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=8 --l1i_assoc=8 --cacheline_size=64 --num-cpus=2
