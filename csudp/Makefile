all:
	clang -O1 udp_client/client.c -lvtllogic -o udp_client/client
	clang -O1 udp_server/server.c -lvtllogic -o udp_server/server
	clang -O1 ping/ping.c  -lvtllogic -o ping/ping_vtl
	cp udp_client/client /usr/bin/s3fudpclient
	cp udp_server/server /usr/bin/s3fudpserver
	cp ping/ping_vtl /usr/bin/s3fping

clean:
	rm -f udp_client/client > /dev/null
	rm -f udp_server/server > /dev/null
	rm -f ping/ping_vtl > /dev/null
	rm -f /usr/bin/s3fping > /dev/null
	rm -f /usr/bin/s3fudpclient > /dev/null
	rm -f /usr/bin/s3fudpserver > /dev/null
