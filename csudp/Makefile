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
	${HOME}/Titan/tools/ttn/ttn.sh activate -p mpi_norm
	clang -O1 -g mpi_norm/mpi_norm.c -lvtllogic -o mpi_norm/mpi_norm
	sudo setcap cap_net_admin,cap_net_raw=eip mpi_norm/mpi_norm
	${HOME}/Titan/tools/ttn/ttn.sh extract -p mpi_norm

tgen:
	${HOME}/Titan/tools/ttn/ttn.sh activate -p tcp_tgen
	clang -O1 -g tcp_tgen/tgen.c -lvtllogic -lm -o tcp_tgen/tgen
	cp tcp_tgen/tgen /usr/bin/tgen
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/tgen
	sudo setcap cap_net_admin,cap_net_raw=eip tcp_tgen/tgen
	${HOME}/Titan/tools/ttn/ttn.sh extract -p tcp_tgen

tgen_incast:
	${HOME}/Titan/tools/ttn/ttn.sh extract -p incast_tgen
	clang -O1 -g tcp_incast_tgen/incast_tgen.c -lvtllogic -lm -lpthread -o tcp_incast_tgen/incast_tgen
	cp tcp_incast_tgen/incast_tgen /usr/bin/incast_tgen
	sudo setcap cap_net_admin,cap_net_raw=eip /usr/bin/incast_tgen
	sudo setcap cap_net_admin,cap_net_raw=eip tcp_incast_tgen/incast_tgen
	${HOME}/Titan/tools/ttn/ttn.sh extract -p incast_tgen

clean:
	rm -f tcp_tgen/tgen > /dev/null
	rm -f /usr/bin/tgen > /dev/null
	rm -f mpi_matrix/mpi_mm > /dev/null
	rm -f mpi_integral/mpi_int > /dev/null
	rm -f mpi_norm/mpi_norm > /dev/null
	rm -f mpi_sat/mpi_csat > /dev/null
	rm -f tcp_incast_tgen/incast_tgen > /dev/null
	rm -f /usr/bin/incast_tgen > /dev/null