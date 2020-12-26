udp:
	clang -O1 udp_client/client.c -lvtllogic -o udp_client/client
	clang -O1 udp_server/server.c -lvtllogic -o udp_server/server
	cp udp_client/client /usr/bin/s3fudpclient
	cp udp_server/server /usr/bin/s3fudpserver

mpi_test:
	clang -O1 -g mpi_mm/mpi_mm.c -lvtllogic -o mpi_mm/mpi_test
	cp mpi_mm/mpi_test /usr/bin/mpi_test
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/mpi_test
	sudo setcap cap_net_admin,cap_net_raw=eip mpi_mm/mpi_test

tgen:
	clang -O1 -g tcp_tgen/tgen.c -lvtllogic -lm -o tcp_tgen/tgen
	cp tcp_tgen/tgen /usr/bin/tgen
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/tgen
	sudo setcap cap_net_admin,cap_net_raw=eip tcp_tgen/tgen


udp_test:
	clang -O1 -g udp/udp_test.c -lvtllogic -o udp/udp_test
	cp udp/udp_test /usr/bin/udp_test
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/udp_test
	sudo setcap cap_net_admin,cap_net_raw=eip udp/udp_test


udp_rate_test:
	clang -O1 -g udp_rate/udp_rate.c -lvtllogic -o udp_rate/udp_rate_test
	cp udp_rate/udp_rate_test /usr/bin/udp_rate_test
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/udp_rate_test
	sudo setcap cap_net_admin,cap_net_raw=eip udp_rate/udp_rate_test

ping:
	clang -O1 ping/ping.c  -lvtllogic -o ping/ping_vtl
	cp ping/ping_vtl /usr/bin/s3fping

tcp_test:
	clang -O1 -g tcp/tcp_test.c -lvtllogic -o tcp/tcp_test
	cp tcp/tcp_test /usr/bin/tcp_test
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/tcp_test
	sudo setcap cap_net_admin,cap_net_raw=eip tcp/tcp_test

clean:
	rm -f mpi_mm/mpi_test > /dev/null
	rm -f /usr/bin/mpi_test > /dev/null
	rm -f udp/udp_test > /dev/null
	rm -f udp_client/client > /dev/null
	rm -f udp_server/server > /dev/null
	rm -f udp_rate/udp_rate_test > /dev/null
	rm -f ping/ping_vtl > /dev/null
	rm -f tcp/tcp_test > /dev/null
	rm -f /usr/bin/s3fping > /dev/null
	rm -f /usr/bin/s3fudpclient > /dev/null
	rm -f /usr/bin/s3fudpserver > /dev/null
	rm -f /usr/bin/tcp_test > /dev/null
	rm -f /usr/bin/udp_test > /dev/null
	rm -f /usr/bin/udp_rate_test > /dev/null
	rm -f tcp_tgen/tgen > /dev/null
	rm -f /usr/bin/tgen > /dev/null
