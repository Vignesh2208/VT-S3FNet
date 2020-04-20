all:
	clang client.c -lvtllogic -o client
	clang server.c -lvtllogic -o server
	#clang ping.c  -lvtllogic -o ping_vtl -mllvm -no-vt-insertion
	#clang ping.c  -o ping_vtl -mllvm -no-vt-insertion
	clang ping.c  -lvtllogic -o ping_vtl
	#sudo chown root:root ping_vtl
	#sudo chmod u+s ping_vtl

clean:
	rm -f client
	rm -f server
	rm -f ping_vtl
