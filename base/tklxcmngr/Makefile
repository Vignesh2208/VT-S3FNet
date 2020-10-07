SRC    		:= tk_lxc_manager.cc lxc_proxy.cc graph_utils.cc virtual_time_manager.cc
CC	   		:= g++
DEBUG  		:= -g -Wno-write-strings

HDR 		:= $(SRC:.cc=.h) 

OBJ  		:= $(SRC:.cc=.o) 

MY_INCLUDES	:= -I../ 
MY_INCLUDES += -I../s3fnet/src
MY_INCLUDES += -I../dml


CFLAGS  := -Wall $(DEBUG) 

all	: lxcmanagermodule.a

lxcmanagermodule.a	: $(OBJ)
	rm -f $@
	ar cq $@ $(OBJ)

%.o :	%.cc $(HDR)
	$(CC) $(CFLAGS) $(MY_INCLUDES) -DENABLED_VT_MANAGER_TITAN -c $< 

print-%  : ; @echo $* = $($*)

	
clean:
	rm -f *.o *.a

