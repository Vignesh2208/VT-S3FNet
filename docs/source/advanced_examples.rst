Advanced Examples
=================


The VT-S3FNet repository also contains some large co-simulation examples.
These examples rely on binaries present in the **~/VT-S3FNet/csudp** directory.



Separate titan projects need to be created for each of these binaries to run
the corresponding co-simulations. Refer to the link 
`here <https://titan-vt.readthedocs.io/en/latest/compilation.html>`_ for information on 
creating and configuring titan projects. 

These emulated applications are briefly described here:

* **cusdup/tcp_tgen**. This folder contains a tcp traffic generator which can generate
  periodic, poisson bursty and constant rate limited traffic. Refer to **tgen.c** file 
  inside the folder for more information on its command line arguments.

* **csudup/tcp_incast_tgen**. This folder contains a tcp traffic generator which can generate
  periodic, poisson bursty and constant rate limited traffic. The number of in-cast to a server
  is also configurable. Refer to **incast_tgen.c** file 
  inside the folder for more information on its command line arguments.

* **csudp/mpi_sat**. This folder contains a program which uses the MPI interface to
  solve the Circuit SAT problem.

* **csudp/mpi_integral**. This folder contains a program which uses the MPI interface to
  solve the parallel integration problem.

* **csudp/mpi_matrix**. This folder contains a program which uses the MPI interface to
  solve the parallel Matrix Vector multiplication problem.


Prior to building/compiling these applications, a unique titan project must
be created for each of them. The following project names are expected.


    ======================      ===========================
    Application                 Expected titan project name
    ======================      ===========================
    csudup/tcp_tgen             tcp_tgen
    csudup/tcp_incast_tgen      incast_tgen
    csudp/mpi_sat               mpi_sat
    csudp/mpi_integral          mpi_integral
    csudup/mpi_matrix           mpi_mm
    ======================      ===========================

.. note:: When creating these projects, make sure the project source directory is correctly specified. Other project options may also be configured as per your needs.


Assuming the previously described set of titan projects have been created, compile the applications::

    cd ~/VT-S3FNet/csudup
    make clean build

Once the previous step is complete, the advanced examples may be run. In particular, two examples are included: 

* **Campus network**. This co-simulation involves emulated tcp traffic generation
  on a large simulated campus network.

* **Fat tree network**. This co-simulation involves emulation of MPI map-reduce style jobs
  on a large simulated fat tree topology.


To run these examples, refer to the files `runTCPExperiments.sh <https://github.com/Vignesh2208/VT-S3FNet/tree/master/base/runTCPExperiments.sh/>`_ and
`runMPIExperiments.sh <https://github.com/Vignesh2208/VT-S3FNet/tree/master/base/runMPIExperiments.sh/>`_.

These scripts launch several co-simulations one after the other. In each co-simulation the type
of workload is changed. Comment out co-simulations which are not needed::

    # Run tcp traffic generation experiments with lookahead enabled
    sudo ./runTCPExperiments.sh 1

    # Run tcp traffic generation experiments with lookahead disabled
    sudo ./runTCPExperiments.sh 0

    # Run MPI workload experiments with lookahead enabled
    sudo ./runMPIExperiments.sh 1

    # Run MPI workload experiments with lookahead disabled
    sudo ./runMPIExperiments.sh 0




