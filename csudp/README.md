Before compiling all these test binaries, you need to create tn projects for each of them.

Step 1. Install Titan

Step 2. Creating Titan projects.

Titan projects can be created with the ttn tool which would be
avaible after titan installation.

General command:

>> ttn add -p <project_name> -s <project_source_directory> [additional options]

For list of additional options:
>> ttn help

E.g, creating a ttn project with the name "mpi_int" for mpi_integral binary

>> ttn add -p mpi_int -s $HOME/VT-S3FNet/csudp/mpi_integral

Following projects are expected to be created:

Project name        Binary (directory in csudp)
1. mpi_mat      ->  mpi_matrix
2. mpi_norm     ->  mpi_norm
3. mpi_sat      ->  mpi_sat
4. incast_tgen  ->  tcp_incast_tgen
5. tcp_tgen     ->  tcp_tgen

After adding all these projects with appropirate options. Next step
is compiling and extracting lookahead from each one. Refer Makefile

E.g to compile and extract lookahead from tcp_tgen, use:

>> sudo make tgen




