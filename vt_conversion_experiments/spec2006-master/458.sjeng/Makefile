SHELL=/bin/sh

# To assist in cross-compiling
LDFLAGS=
CFLAGS=-Wall -Winline -O2 -fpic $(BIGFILES) -DSPEC_CPU -mno-red-zone

# Where you want it installed when you do 'make install'
PREFIX=/usr/local

OBJS= attacks.o book.o crazy.o draw.o ecache.o epd.o eval.o leval.o \
	  moves.o neval.o partner.o proof.o rcfile.o search.o see.o seval.o \
	  ttable.o utils.o sjeng.o

all: sjeng 

sjeng: $(OBJS)

ifeq ($(CC), gcc)
	$(CC) $(CFLAGS) -o sjeng_gcc $(OBJS) $(LDFLAGS) $(VTFLAGS)
else
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS) $(VTFLAGS)
endif

clean: 
	rm -f *.o *.B *.i *.I *.O *.spin sjeng
