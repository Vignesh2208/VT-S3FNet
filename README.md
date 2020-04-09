# VT-S3FNet
S3FNet with virtual time support from Titan


IMPORTANT:
To get lxc-start to work, Apparmor profile must be disabled.

>>  sudo ln -s /etc/apparmor.d/usr.bin.lxc-start /etc/apparmor.d/disable/
>>  sudo apparmor_parser -R /etc/apparmor.d/usr.bin.lxc-start

Verify that lxc-start profile no longer exists with the following command:

>> sudo aa-status

Dependencies:

Install flex
