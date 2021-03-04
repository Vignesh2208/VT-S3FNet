# VT-S3FNet
S3FNet with virtual time support for Titan and Kronos

Step-1. Install Dependencies:

Install Titan
Install flex
Install lxc
Install tunctl
Install iptables


IMPORTANT:
To get lxc-start to work, Apparmor profile must be disabled.

>>  sudo ln -s /etc/apparmor.d/usr.bin.lxc-start /etc/apparmor.d/disable/
>>  sudo apparmor_parser -R /etc/apparmor.d/usr.bin.lxc-start

Verify that lxc-start profile no longer exists with the following command:

>> sudo aa-status


Step-2. Building and Install:

>> cd ~/VT-S3FNet/base
>> sudo make clean fullbuild

Optional (Building for Kronos instead of Titan):

Before the fullbuild step, remove all defines "-DENABLED_VT_MANAGER_TITAN" in all makefiles
inside the base directory.

Step-3. Building experiment test binaries.

These are located inside csudp directory. Refer to the README instructions
inside that directory.



