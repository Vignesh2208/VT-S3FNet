User Guide
==========

This section describes how to specify co-simulated models using the 
Domain Modelling Language (DML). The reader is assumed to have some
familiarity with S3FNet specific DML constructs described 
`here <https://s3f.iti.illinois.edu/usrman/s3fnet.html#dml>`_.


Throughout this section, we will use a running example defined
`here <https://github.com/Vignesh2208/VT-S3FNet/tree/master/base/s3fnet/test/lxc_tests/small_2_tcp_large_pings/test.dml/>`_.

This is copied below for convenience::

    total_timeline 5	
    tick_per_second 6	
    run_time 5
    seed 1	
    log_dir "4_LXC_Small_TCP"		
    virtual_time_manager "TITAN"
    eat_update_period_us 1000
    enable_lookahead 1

    # ------------- CO-SIMULATION TOPOLOGY ------------------#
    #     client                                  server     #
    #       1us\  1us links                      /1us        #
    #           r0--r1--r2--r3--r4--r5--r6--r7--r8           #
    #       1us/                                 \1us        #
    #     client                                  server     #
    #--------------------------------------------------------#


    Net
    [
        lxcConfig
        [		
            # Poisson bursty flows between client server pairs
            settings [ lxcNHI 0:0 ttnProject "tcp_tgen" dependants "1" cmd "/home/titan/VT-S3FNet/csudp/tcp_tgen/tgen client 1:0 7891 poisson 100000 > /tmp/client1.log"  ]
            settings [ lxcNHI 1:0 ttnProject "tcp_tgen" dependants "0" cmd "/home/titan/VT-S3FNet/csudp/tcp_tgen/tgen server 1:0 7891 > /tmp/server1.log"  ]
            settings [ lxcNHI 2:0 ttnProject "tcp_tgen" dependants "3" cmd "/home/titan/VT-S3FNet/csudp/tcp_tgen/tgen client 3:0 7891 poisson 100000 > /tmp/client2.log"  ]
            settings [ lxcNHI 3:0 ttnProject "tcp_tgen" dependants "2" cmd "/home/titan/VT-S3FNet/csudp/tcp_tgen/tgen server 3:0 7891 > /tmp/server2.log"  ]

        ]	
        
        Net 
        [ 
            id 0
            alignment 0
            host 																	# Host 0:0
            [ 
                id 0
                _extends .dict.emuHost
            ]
        ]
        Net 
        [ 
            id 1
            alignment 1
            host 																	# Host 1:0
            [ 
                id 0
                _extends .dict.emuHost
            ]
        ]
        Net 
        [ 
            id 2
            alignment 2
            host 																	# Host 0:0
            [ 
                id 0
                _extends .dict.emuHost
            ]
        ]
        Net 
        [ 
            id 3
            alignment 3
            host 																	# Host 1:0
            [ 
                id 0
                _extends .dict.emuHost
            ]
        ]
        Net 
        [ 
            id 4
            alignment 4		
            router																	# Router 1:2
            [
                id 0
                _find .dict.routerGraph.graph
                interface [id 0 _extends .dict.1Gb]
                interface [id 1 _extends .dict.1Gb]
                interface [id 2 _extends .dict.1Gb]
            ]
            router																	# Router 1:2
            [
                id 1
                _find .dict.routerGraph.graph
                interface [id 0 _extends .dict.1Gb]
                interface [id 1 _extends .dict.1Gb]
            ]
                router																	# Router 1:2
            [
                id 2
                _find .dict.routerGraph.graph
                interface [id 0 _extends .dict.1Gb]
                interface [id 1 _extends .dict.1Gb]
            ]
                router																	# Router 1:2
            [
                id 3
                _find .dict.routerGraph.graph
                interface [id 0 _extends .dict.1Gb]
                interface [id 1 _extends .dict.1Gb]
            ]
            router																	# Router 1:2
            [
                id 4
                _find .dict.routerGraph.graph
                interface [id 0 _extends .dict.1Gb]
                interface [id 1 _extends .dict.1Gb]
            ]	
            router																	# Router 1:2
            [
                id 5
                _find .dict.routerGraph.graph
                interface [id 0 _extends .dict.1Gb]
                interface [id 1 _extends .dict.1Gb]
            ]	
            router																	# Router 1:2
            [
                id 6
                _find .dict.routerGraph.graph
                interface [id 0 _extends .dict.1Gb]
                interface [id 1 _extends .dict.1Gb]
            ]
            router																	# Router 1:2
            [
                id 7
                _find .dict.routerGraph.graph
                interface [id 0 _extends .dict.1Gb]
                interface [id 1 _extends .dict.1Gb]
            ]
            router																	# Router 1:2
            [
                id 8
                _find .dict.routerGraph.graph
                interface [id 0 _extends .dict.1Gb]
                interface [id 1 _extends .dict.1Gb]
                interface [id 2 _extends .dict.1Gb]
            ]
        ]

        # Host to router links
        link [ attach 0:0(0) attach 4:0(0) _extends .dict.link_delay_1us ]
        link [ attach 1:0(0) attach 4:8(1) _extends .dict.link_delay_1us ]
        link [ attach 2:0(0) attach 4:0(2) _extends .dict.link_delay_1us ]
        link [ attach 3:0(0) attach 4:8(2) _extends .dict.link_delay_1us ]

        # Router - router links
        link [ attach 4:0(1) attach 4:1(0) _extends .dict.link_delay_1us ]
        link [ attach 4:1(1) attach 4:2(0) _extends .dict.link_delay_1us ]
        link [ attach 4:2(1) attach 4:3(0) _extends .dict.link_delay_1us ]
        link [ attach 4:3(1) attach 4:4(0) _extends .dict.link_delay_1us ]
        link [ attach 4:4(1) attach 4:5(0) _extends .dict.link_delay_1us ]
        link [ attach 4:5(1) attach 4:6(0) _extends .dict.link_delay_1us ]
        link [ attach 4:6(1) attach 4:7(0) _extends .dict.link_delay_1us ]
        link [ attach 4:7(1) attach 4:8(0) _extends .dict.link_delay_1us ]	
    ]





This file defines a simple co-simulation consisting of 4 emulated hosts (LXCs)
interacting with each other over a simulated network consisting of 8 routers.

A detailed tutorial on how to define S3FNet simulation models using
DML is available `here <http://www.ssfnet.org/InternetDocs/ssfnetTutorial-1.html>`_.

In this section, we only describe additional fields specifically added to the DML language to 
support **co-simulation**. These fields are described below:

* **total_timeline**. Total number of timelines in the co-simulation. The running example contains 5
  timelines.

* **tick_per_second**. Number of ticks in one second. This controls the time resolution. Setting it 
  to a value 6 represents 10^6 ticks in one second. Thus each tick represents 1us. Currently the highest
  resolution supported in a co-simulation is 1us.

* **log_dir**. Specifies a directory which is created inside ~/VT-S3FNet/experiment-data. Any experiment
  logs are stored here.

* **run_time**. Total virtual run time of the co-simulation in seconds.

* **virtual_time_manager**. This field can take the value either "TITAN" or "KRONOS". Note that
  VT-3FNet must have been installed for the chosen virtual time manager. In the running example
  Titan is chosen as the virtual time manager. 

* **eat_update_period_us**. This field is relevant only when Titan is the chosen virtual time 
  manager. It controls the earliest arrival time update frequency. This is only relevant when
  lookaheads are enabled. In the running example, this is set to 1ms.

* **enable_lookahead**. This field is relevant only when Titan is chosen as the virtual time
  manager. If set to 1, then lookahead based synchronization would be used. If set to 0, lookaheads
  would be ignored.

* **lxcConfig**. This field groups settings for all emulated hosts/LXCs in the co-simulation.
  Each emulated host is configured with a separate **settings** attribute as illustrated in the
  running example.

* **lxcNHI**. This field identifies the specific LXC in question. It is folowed by two numbers separated
  by a colon (e.g 0:0). These numbers should be interpreted as network-id:host-id i.e they refer to 
  a specific network and a specific host aligned on the network. Thus 0:0 refers to host with id 0 aligned
  on a network with id 0.

* **ttnProject**. This field specifies the titan project associated with code that needs to be emulated on
  the lxc in question. For information on titan projects, refer this link. It may be left un-specified if the 
  virtual time manager used is Kronos. 

  In the running example, a project with the name "tcp_tgen" is assumed to exist before running this co-simulation.
  It is also assumed that the binary ~/VT-S3FNet/csudp/tcp_tgen/tgen has been compiled with under this titan project.


* **dependants**. This field specifies a comma separated list of timelines which may influence/affect the LXC in
  question. For instance, in the running example, lxc 0:0 can be influenced by any emulated host aligned on timeline 1 and 
  lxc 1:0 can be influenced by any emulated host aligned on timeline 0. 

  If left un-specified, then an lxc is assumed to depend on all timelines hosting other lxcs.
  Multiple dependants may be specified as a comma separated string (e.g "1,2,3,4").
  This field is ignored if the virtual time manager is Kronos.

* **cmd**. This field specifies the command to emulate on the host/lxc in question.


Emulated host definitions
^^^^^^^^^^^^^^^^^^^^^^^^^

The previous section described how to specify commands to be co-simulated. The next crucial step involves
attaching a proxy for each emulated host in the simulated network. This is done by adding definitions
of each emulated host.

An example is given below::

	Net 
	[ 
		id 0          # Network-id
		alignment 0   # Timeline on which this network and all its hosts are aligned
		host 																	# Host 0:0
		[ 
			id 0      # host 0 of this network.
			_extends .dict.emuHost  # emuHost indicates that this host is emulated.
		]

        # Note that more host definitions may be added here. But they must all be emulated as well.
        # If one host aligned on a network is emulated, then all other hosts aligned on the network
        # must also be emulated.
	]

This example adds an emulated host on a network with id-0. The emulated host's id is also 0.
This host is aligned to timeline 0 (since aligment is 0). This proxy definition corresponds to lxcNHI 0:0
and its configuration.

Similarly the example below corresponds to lxcNHI 1:0::

	Net 
	[ 
		id 1
		alignment 1
		host 																	# Host 1:0
		[ 
			id 0
			_extends .dict.emuHost
		]
	]

The **emuHost** definition can be found `here <https://github.com/Vignesh2208/VT-S3FNet/tree/master/base/s3fnet/test/lxc_tests/aux/mydictionary.dml/>`_.
This is expected to be common among all emulated hosts. It defines the ProtocolSession to be used for emulated hosts.

.. note:: The current implementation requires all hosts aligned on a timeline to be exclusively emulated or simulated i.e, they cannot be a mix of both. Futher, the lookahead algorithm currently only supports alignment of simulated hosts to one timeline.

.. note:: In the running example, lxcs 0:0, 1:0, 2:0 and 3:0 are aligned on timelines 0, 1, 2 and 3 respectively. These timelines only host emulated entities.

Defining a simulated network
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simulated networks may be created as described in the S3FNet and SSFNet tutorials.

* A key restriction is that all simulated network-ids must be aligned to the same timeline.

* No emulated host must be aligned to this timeline

In the running example, the simulated network is defined separately and aligned onto one timeline::


    Net 
	[ 
		id 4           # Network id 4 contains only simulated routers.
		alignment 4	 	
		router																	# Router 1:2
		[
			id 0
			_find .dict.routerGraph.graph
			interface [id 0 _extends .dict.1Gb]
			interface [id 1 _extends .dict.1Gb]
			interface [id 2 _extends .dict.1Gb]
		]
		router																	# Router 1:2
		[
			id 1
			_find .dict.routerGraph.graph
			interface [id 0 _extends .dict.1Gb]
			interface [id 1 _extends .dict.1Gb]
		]
		router																	# Router 1:2
		[
			id 2
			_find .dict.routerGraph.graph
			interface [id 0 _extends .dict.1Gb]
			interface [id 1 _extends .dict.1Gb]
		]
		router																	# Router 1:2
		[
			id 3
			_find .dict.routerGraph.graph
			interface [id 0 _extends .dict.1Gb]
			interface [id 1 _extends .dict.1Gb]
		]
		router																	# Router 1:2
		[
			id 4
			_find .dict.routerGraph.graph
			interface [id 0 _extends .dict.1Gb]
			interface [id 1 _extends .dict.1Gb]
		]	
		router																	# Router 1:2
		[
			id 5
			_find .dict.routerGraph.graph
			interface [id 0 _extends .dict.1Gb]
			interface [id 1 _extends .dict.1Gb]
		]	
		router																	# Router 1:2
		[
			id 6
			_find .dict.routerGraph.graph
			interface [id 0 _extends .dict.1Gb]
			interface [id 1 _extends .dict.1Gb]
		]
		router																	# Router 1:2
		[
			id 7
			_find .dict.routerGraph.graph
			interface [id 0 _extends .dict.1Gb]
			interface [id 1 _extends .dict.1Gb]
		]
		router																	# Router 1:2
		[
			id 8
			_find .dict.routerGraph.graph
			interface [id 0 _extends .dict.1Gb]
			interface [id 1 _extends .dict.1Gb]
			interface [id 2 _extends .dict.1Gb]
		]
	]

This defines a simulated network containing 8 routers. This network
is aligned on timeline 4.

The running example also defines links interconnecting all the emulated
and simulated entities in the co-simulation. This is based on the S3FNet
DML specification and is explained futher in the linked tutorials.


Running the co-simulation
^^^^^^^^^^^^^^^^^^^^^^^^^

To run a co-simulation, the dml file (such as the one above) must be placed in a 
directory containing a makefile such as the one linked
`here <https://github.com/Vignesh2208/VT-S3FNet/tree/master/base/s3fnet/test/lxc_tests/small_2_tcp_large_pings/Makefile/>`_. 


Please follow this template to define makefiles for other co-simulations as well.

.. note:: Before running a co-simulation, make sure that the corresponding virtual time manager (Titan or Kronos) is loaded.

To run a co-simulation, use the following commands::

    cd <co-simulated-mode-definition-directory>
    make clean
    make
    make test


For instance to run this example::

    cd ~/VT-S3FNet/base/s3fnet/test/lxc_tests/small_2_tcp_large_pings
    make clean
    make
    make test









