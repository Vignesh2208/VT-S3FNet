#!/bin/bash

USAGE="Usage: `basename $0` [-h] [-n arg] [-f] [-i] [-d] [-t]" 
PARAMETER="-n\t number of cores used to run make\n-f\t skip building those libraries that only need to be built once (DML, metis)\n-i\t incremental build (update) instead of clean build\n-d\t display S3FNet debug messages\n-t\t Build with Titan\n-h\t display the usage"
OVERVIEW="Script for building the S3F project"
EXAMPLE="e.g., `basename $0` -n 4 -f \n Use 4 cores to clean build the S3F project excluding those libraries that only need to be built once"

#default values
nc=1  # number core used to build the project = 1
dml=1 # to build dml  
inc=0 # no incremental build, i.e., clean build
debug=0 # not show s3fnet debug messages
titan=0

# Parse command line options
while getopts hn:fidt OPT; do
    case "$OPT" in 
        h)
            echo $OVERVIEW
            echo $USAGE
            echo $PARAMETER
            echo $EXAMPLE
            exit 0
            ;;
        n)
            nc=$OPTARG
            if [ $nc -le 0 ]; then
                nc=1
            fi
            ;;
        f)
            dml=0
            ;;
        d)
            debug=1
            ;;
        i)
            inc=1
            ;;
        t)  titan=1
            ;;
        \?)
            # getopts issues an error message
            echo $OVERVIEW
            echo $USAGE >&2
            echo $PARAMETER
            echo $EXAMPLE
            exit 1
            ;;
        esac
done




SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

sed "s|@BASE_DIR@|${BASE_DIR}|g" s3fnet-definitions.template > s3fnet-definitions.h

# Remove the switches we parsed above
shift `expr $OPTIND - 1`

echo "--------------------------------"
echo "Buidling Lxc-Manager ... "
echo "--------------------------------"
cd tklxcmngr
make clean
make
cd ..

echo "--------------------------------"
echo "Buidling s3f/api ... "
echo "--------------------------------"
cd api
if [ $inc -eq 0 ]; then
rm -f *.o *.a > /dev/null
fi
make -j$nc
cd ..

echo "--------------------------------"
echo "Buidling s3f/rng ... "
echo "--------------------------------"
cd rng
if [ $inc -eq 0 ]; then
rm -f *.o *.a > /dev/null
fi
make -j$nc
cd ..

echo "--------------------------------"
echo "Buidling s3f/aux ... "
echo "--------------------------------"
cd aux
if [ $inc -eq 0 ]; then
rm -f *.o *.a > /dev/null
fi
make -j$nc
cd ..

#echo "--------------------------------"
#echo "Buidling s3f/app ... "
#echo "--------------------------------"
#cd app
#if [ $inc -eq 0 ]; then
#rm *.o
#fi
#make
#cd ..



echo "DML = ", $dml
echo "INC = ", $inc
if [ $dml -eq 1 ] && [ $inc -eq 0 ]; then
echo "--------------------------------"
echo "Buidling s3f/dml ... "
echo "--------------------------------"
cd dml
aclocal
autoconf
automake
automake --add-missing
./configure CFLAGS=-Wno-write-strings
make clean
make
cd ..
fi

echo "--------------------------------"
echo "Buidling s3f/metis ... "
echo "--------------------------------"
cd metis
rm *.o *.a 
sh metis.sh
cd ..

echo "--------------------------------"
echo "Buidling s3f/s3fnet ... "
echo "--------------------------------"
cd s3fnet
if [ $inc -eq 0 ]; then
make clean
fi
if [ $debug -eq 0 ]; then
arg="$arg ENABLE_S3FNET_DEBUG=no"
else
arg="$arg ENABLE_S3FNET_DEBUG=yes"
fi

if [ $debug -eq 1 ]; then
arg="$arg ENABLED_VT_MANAGER_TITAN=1"
fi
echo "ARG = "
echo $arg
make -j$nc $arg
cd ..
