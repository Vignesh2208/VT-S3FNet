udp:
	clang -O1 udp_client/client.c -lvtllogic -o udp_client/client
	clang -O1 udp_server/server.c -lvtllogic -o udp_server/server
	cp udp_client/client /usr/bin/s3fudpclient
	cp udp_server/server /usr/bin/s3fudpserver

ping:
	clang -O1 ping/ping.c  -lvtllogic -o ping/ping_vtl
	cp ping/ping_vtl /usr/bin/s3fping

tcp_test:
	clang -O1 -g tcp/tcp_test.c -lvtllogic -o tcp/tcp_test
	cp tcp/tcp_test /usr/bin/tcp_test
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/tcp_test
	sudo setcap cap_net_admin,cap_net_raw=eip tcp/tcp_test

clean:
	rm -f udp_client/client > /dev/null
	rm -f udp_server/server > /dev/null
	rm -f ping/ping_vtl > /dev/null
	rm -f tcp/tcp_test > /dev/null
	rm -f /usr/bin/s3fping > /dev/null
	rm -f /usr/bin/s3fudpclient > /dev/null
	rm -f /usr/bin/s3fudpserver > /dev/null
	rm -f /usr/bin/tcp_test > /dev/null
