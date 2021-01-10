SHELL=/bin/sh

# To assist in cross-compiling
CC:=clang
AR:=ar
RANLIB:=ranlib
VTFLAGS=-lvtllogic
CLANG_LLVM_FLAGS=-mllvm -no-vt-insertion
CD:=cd
RM:=rm

export

multiply:
	@echo 'Activating ttn mmultiply project ...'
	@${HOME}/Titan/tools/ttn/ttn.sh activate -p mmultiply
	@$(CD) mmultiply && make clean build

bzip2:
	@echo 'Activating ttn bzip2 project ...'
	@${HOME}/Titan/tools/ttn/ttn.sh activate -p bzip2
	@$(CD) 401.bzip2 && make clean bzip2

sjeng:
	@echo 'Activating ttn sjeng project ...'
	@${HOME}/Titan/tools/ttn/ttn.sh activate -p sjeng
	@$(CD) 458.sjeng && make clean sjeng

h264ref:
	@echo 'Activating ttn h264ref project ...'
	@${HOME}/Titan/tools/ttn/ttn.sh activate -p h264ref
	@$(CD) 464.h264ref && make clean h264ref

all: bzip2 sjeng h264ref mmultiply

clean:
	@$(CD) 401.bzip2 && make clean
	@$(CD) 458.sjeng && make clean
	@$(CD) 464.h264ref && make clean
	@$(CD) mmultiply && make clean


