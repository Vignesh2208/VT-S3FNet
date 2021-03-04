

SHELL=/bin/sh

RM:=rm
# To assist in cross-compiling
LDFLAGS=

BIGFILES=-D_FILE_OFFSET_BITS=64
CFLAGS=-Wall -Winline -O2 -fpic -g $(BIGFILES) -DSPEC_CPU -mno-red-zone

# Where you want it installed when you do 'make install'
PREFIX=/usr/local




build:
ifeq ($(CC), gcc)
	$(CC) $(CFLAGS) -o mmultiply_gcc mmultiply.c
else
	$(CC) $(CFLAGS) -o mmultiply mmultiply.c -lvtllogic -O1 -mno-red-zone
endif

clean:
	@rm -f mmultiply > /dev/null
	@rm -f mmultiply_gcc > /dev/null
