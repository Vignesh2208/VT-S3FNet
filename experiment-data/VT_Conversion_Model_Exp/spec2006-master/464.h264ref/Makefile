SHELL=/bin/sh

# To assist in cross-compiling
LDFLAGS=-lm
CFLAGS=-Wall -fpic -O2 -DSPEC_CPU -mno-red-zone

# Where you want it installed when you do 'make install'
PREFIX=/usr/local

OBJS= annexb.o biariencode.o block.o cabac.o configfile.o context_ini.o \
		 decoder.o explicit_gop.o fast_me.o filehandle.o fmo.o header.o image.o \
		 intrarefresh.o leaky_bucket.o lencod.o loopFilter.o macroblock.o \
		 mb_access.o mbuffer.o memalloc.o mv-search.o nal.o nalu.o nalucommon.o \
		 output.o parset.o parsetcommon.o q_matrix.o q_offsets.o ratectl.o \
		 rdopt.o rdopt_coding_state.o rdpicdecision.o refbuf.o rtp.o sei.o \
		 slice.o transform8x8.o vlc.o weighted_prediction.o specrand.o

all: h264ref

h264ref: $(OBJS)
ifeq ($(CC), gcc)
	$(CC) $(CFLAGS) -o h264ref_gcc $(OBJS) $(LDFLAGS) $(VTFLAGS)
else
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS) $(VTFLAGS)
endif

clean: 
	rm -f *.o *.B *.i *.I *.O *.spin h264ref
