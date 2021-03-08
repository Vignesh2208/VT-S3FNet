Installation
============

Minimum System Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^

VT-S3FNet has been tested on Ubuntu 16.04.5 and 18.04 LTS. It is advisable to run it on a 
system or VM with atleast 4 cores and 4GB of RAM.

* Default python version on the system must be >= 3.6.9


Installing Common Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install flex::

    sudo apt-get install flex

* Install lxc version 3.0.3::

    wget -P ~/Downloads https://linuxcontainers.org/downloads/lxc/lxc-3.0.3.tar.gz
    tar -xvf ~/Downloads/lxc-3.0.3.tar.gz
    cd ~/Downloads/lxc-3.0.3
    ./configure
    sudo make install

  To get lxc-start to work, Apparmor profile must be disabled::

    sudo ln -s /etc/apparmor.d/usr.bin.lxc-start /etc/apparmor.d/disable/
    sudo apparmor_parser -R /etc/apparmor.d/usr.bin.lxc-start

  Verify that lxc-start profile no longer exists with the following command::

    sudo aa-status

* Install tunctl::

    sudo apt-get install uml-utilities bridge-utils

* Install iptables::

    sudo apt-get install iptables


VT-S3FNet can work with **Titan** and **Kronos**. The installation procedure
varies slightly depending on which virtual time system is used. 


Installation with Titan
^^^^^^^^^^^^^^^^^^^^^^^

To get started, perform the following steps:

* Install Titan using the installation steps described here.

* Clone the VT-S3FNet repository::

    git clone https://github.com/Vignesh2208/VT-S3FNet.git

* Build and install::

    cd ~/VT-S3FNet
    sudo make clean fullbuild

Installation with Kronos
^^^^^^^^^^^^^^^^^^^^^^^^

To get started, perform the following steps:

* Install Kronos using the installation steps described here.

* Clone the VT-S3FNet repository::

    git clone https://github.com/Vignesh2208/VT-S3FNet.git

* Before the fullbuild step, remove all defines "-DENABLED_VT_MANAGER_TITAN" in all
  makefiles inside the ~/VT-S3FNet/base directory. This may be done with the
  following command::

    find ~/VT-S3FNet/base -type f -exec sed -i 's/DENABLED_VT_MANAGER_TITAN/UENABLED_VT_MANAGER_TITAN/g' {} \;

  

* Build and install::

    cd ~/VT-S3FNet
    sudo make clean fullbuild

    
Ready to use VM
^^^^^^^^^^^^^^^

Instuctions to Follow.
