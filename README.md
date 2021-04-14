# VT-S3FNet
S3FNet with virtual time support for Titan and Kronos.


Full documentation can be found [here](https://vt-s3fnet.readthedocs.io/en/latest/index.html)

Note
====

This is a prototype implementation with the primary goal of encouraging more research in the field of virtual time driven network emulation and simulation.
It does not support all general requirements yet and may contain bugs. Contributions to fix any identified issues are welcome ! Please contact me at vig2208@gmail.com


TODO
====

Investigate/BUG-FIX: There appears to be slight differences between packet send timestamps when lookaheads are used vs when lookaheads are disabled. Infact it appears that we don't have perfect repeatability across two runs of the same experiment regarless of whether lookaheads are enabled or disabled. This may be a bug in the implementation or it could be because of some randomness introduced by the kernel due to transferring packets using linux bridges and tap devices. This phenomenon needs more careful investigation. As of v1.0.1 the cause of this is unclear.

