SHELL=/bin/sh

RM:=rm
# To assist in cross-compiling
LDFLAGS=

BIGFILES=-D_FILE_OFFSET_BITS=64
CFLAGS=-Wall -Winline -O2 -fpic -g $(BIGFILES) -DSPEC_CPU -mno-red-zone

# Where you want it installed when you do 'make install'
PREFIX=/usr/local


OBJS= spec.o       \
	  blocksort.o  \
      huffman.o    \
      crctable.o   \
      randtable.o  \
      compress.o   \
      decompress.o \
      bzlib.o

all: libbz2.so bzip2 

bzip2: libbz2.so bzip2.o
ifeq ($(CC), gcc)
	$(CC) $(CFLAGS) -o bzip2_gcc bzip2.o -L. -lbz2gcc $(VTFLAGS) $(LDFLAGS)
else
	$(CC) $(CFLAGS) -o bzip2 bzip2.o -L. -lbz2 $(VTFLAGS) $(LDFLAGS) $(CLANG_LLVM_FLAGS)
	#$(CC) $(CFLAGS) -o bzip2 bzip2.o -L. -lbz2 $(CLANG_LLVM_FLAGS)
endif

bzip2recover: bzip2recover.o
ifeq ($(CC), gcc)
	$(CC) $(CFLAGS) -o bzip2recover_gcc bzip2recover.o $(VTFLAGS) $(LDFLAGS)
else
	$(CC) $(CFLAGS) -o bzip2recover bzip2recover.o $(VTFLAGS) $(LDFLAGS) $(CLANG_LLVM_FLAGS)
	#$(CC) $(CFLAGS) -o bzip2recover bzip2recover.o $(CLANG_LLVM_FLAGS)
endif
	
libbz2.so: $(OBJS)
	@$(RM) -f libbz2.so
	@$(RM) -f libbz2gcc.so
ifeq ($(CC), gcc)
	$(CC) -w -shared -o libbz2gcc.so $(OBJS)
	@sudo cp -v libbz2gcc.so /usr/local/lib
else
	$(CC) -w -shared -o libbz2.so $(OBJS) $(CLANG_LLVM_FLAGS)
	#$(CC) -w -shared -o libbz2.so $(OBJS) $(CLANG_LLVM_FLAGS)
	@sudo cp -v libbz2.so /usr/local/lib
endif

#libbz2.a: $(OBJS)
#	$(RM) -f libbz2.a
#	$(AR) cq libbz2.a $(OBJS)
#	@if ( test -f $(RANLIB) -o -f /usr/bin/ranlib -o \
#		-f /bin/ranlib -o -f /usr/ccs/bin/ranlib ) ; then \
#		echo $(RANLIB) libbz2.a ; \
#		$(RANLIB) libbz2.a ; \
#	fi

clean: 
	rm -f *.o *.B *.i *.I *.O *.spin libbz2.so libbz2.a bzip2 
