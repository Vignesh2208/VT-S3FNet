# -- an example to run SPEC 429.mcf on gem5, put it under 429.mcf folder --
#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export GEM5_DIR=/home/titan/gem5
export BENCHMARK=$DIR/h264ref_gcc


#mkdir -p m5out


#time $GEM5_DIR/build/X86/gem5.opt -d $DIR/m5out $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 1000000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64


#mkdir -p m5out-2


#time $GEM5_DIR/build/X86/gem5.opt -d $DIR/m5out-2 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c2.cfg' -I 1000000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64


#mkdir -p m5out-3


#time $GEM5_DIR/build/X86/gem5.opt -d $DIR/m5out-3 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c3.cfg' -I 1000000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64


mkdir -p insout-100


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-100 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 100000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64


mkdir -p insout-200


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-200 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 200000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64


mkdir -p insout-300


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-300 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 300000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64


mkdir -p insout-400


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-400 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 400000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64

mkdir -p insout-500


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-500 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 500000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64

mkdir -p insout-600


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-600 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 600000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64

mkdir -p insout-700


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-700 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 700000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64

mkdir -p insout-800


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-800 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 800000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64

mkdir -p insout-900


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-900 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 900000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64

mkdir -p insout-1000


time $GEM5_DIR/build/X86/gem5.opt -d $DIR/insout-1000 $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o '-d /home/titan/Tomacs-2020/spec2006-master/464.h264ref/h264ref_c1.cfg' -I 1000000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --cacheline_size=64
