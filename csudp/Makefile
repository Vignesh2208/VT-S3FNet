udp:
	clang -O1 udp_client/client.c -lvtllogic -o udp_client/client
	clang -O1 udp_server/server.c -lvtllogic -o udp_server/server
	cp udp_client/client /usr/bin/s3fudpclient
	cp udp_server/server /usr/bin/s3fudpserver


mpi_mat:
	${HOME}/Titan/tools/ttn/ttn.sh activate -p mpi_mat
	clang -O1 -g mpi_matrix/mpi_mm.c -lvtllogic -o mpi_matrix/mpi_mm
	sudo setcap cap_net_admin,cap_net_raw=eip mpi_matrix/mpi_mm
	${HOME}/Titan/tools/ttn/ttn.sh extract -p mpi_mat

mpi_int:
	${HOME}/Titan/tools/ttn/ttn.sh activate -p mpi_int
	clang -O1 -g mpi_integral/mpi_int.c -lvtllogic -lm -o mpi_integral/mpi_int
	sudo setcap cap_net_admin,cap_net_raw=eip mpi_integral/mpi_int
	${HOME}/Titan/tools/ttn/ttn.sh extract -p mpi_int

mpi_csat:
	${HOME}/Titan/tools/ttn/ttn.sh activate -p mpi_sat
	clang -O1 -g mpi_sat/mpi_csat.c -lvtllogic -o mpi_sat/mpi_csat
	sudo setcap cap_net_admin,cap_net_raw=eip mpi_sat/mpi_csat
	${HOME}/Titan/tools/ttn/ttn.sh extract -p mpi_sat

mpi_inf_norm:
	clang -O1 -g mpi_norm/mpi_norm.c -lvtllogic -o mpi_norm/mpi_norm
	sudo setcap cap_net_admin,cap_net_raw=eip mpi_norm/mpi_norm

tgen:
	clang -O1 -g tcp_tgen/tgen.c -lvtllogic -lm -o tcp_tgen/tgen
	cp tcp_tgen/tgen /usr/bin/tgen
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/tgen
	sudo setcap cap_net_admin,cap_net_raw=eip tcp_tgen/tgen

tgen_incast:
	clang -O1 -g tcp_incast_tgen/incast_tgen.c -lvtllogic -lm -lpthread -o tcp_incast_tgen/incast_tgen
	cp tcp_incast_tgen/incast_tgen /usr/bin/incast_tgen
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/incast_tgen
	sudo setcap cap_net_admin,cap_net_raw=eip tcp_incast_tgen/incast_tgen


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
	rm -f mpi_matrix/mpi_mat > /dev/null
	rm -f mpi_integral/mpi_int > /dev/null
	rm -f mpi_norm/mpi_norm > /dev/null
	rm -f mpi_sat/mpi_csat > /dev/null
	rm -f tcp_incast_tgen/incast_tgen > /dev/null
	r -f /usr/bin/incast_tgen > /dev/null