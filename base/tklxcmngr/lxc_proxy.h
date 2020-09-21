/**
 * \file lxc_proxy.h
 *
 * \brief LXC Proxy
 *
 * authors : Vignesh Babu
 */

#ifndef __TIMEKEEPER_LXCPROXY_H__
#define __TIMEKEEPER_LXCPROXY_H__

#include <sys/types.h>		// O_RDWR
#include <sys/stat.h>		// O_RDWR
#include <fcntl.h>			// O_RDWR
#include <queue>
#include <mutex>

#include <unistd.h> 		// close
//#include <linux/if.h>
//#include <linux/if_tun.h>
//#include <sys/ioctl.h>	


#define TIME_200_MS_IN_US           200000
#define TIME_100_MS_IN_US           100000

#define NS_IN_SECS 1000000000



enum LxcCommand {
	LXC_CREATE,
	LXC_STOP,
	LXC_DESTROY,
	LXC_START_TRACER,
	LXC_START_PRODUCER

};

class LxcManager;
class LXC_Proxy;

typedef std::pair<long long, int> lPair; 



/*
 ******************************************************************************
 * Emu Packet Class - contains information about packet that is captured by 
 * LXC Proxy Through a TAP device
 ******************************************************************************
 */

class EmuPacket
{
	public:

		int     len;                        // packet length in bytes
		ltime_t outgoingTime;
		ltime_t incomingTime;

		u_short ethernetType;
		int     incomingFD;
		int     outgoingFD;

		unsigned char *data;                // packet payload pointer

		LXC_Proxy * destProxy;				// pointer to destProxy which should recv packet

		EmuPacket(int len);                 // contructor
		virtual ~EmuPacket();               // destructor
		EmuPacket* duplicate();             // generate an extra copy of this packet, for multicast
};

/*
 ******************************************************************************
 * LXC Proxy mediates the travel of packets between LXCs and the Simulator
 ******************************************************************************
 */
class LXC_Proxy
{
	public:

		//---------------------------------------------------------------------
		// 				Constructors / Destructor
		//---------------------------------------------------------------------

		/*
		 * Constructor.
		 * 1st Param - NHI of the S3FNet Host which will be emulated
		 * 2nd Param - The IP address of the S3FNet Host that will be emulated
		 * Note: careful with changing the host/network order
		 * 3rd Param - Pointer to the LXC Manager
		 * 4th Param - Timeline this LXC is aligned on
		 * TODO: 4th Param can be replaced with actual ID
		 */
		LXC_Proxy(string, unsigned int, LxcManager* c, Timeline* timeline);

		/*
		 * Destructor.
		 * Stops an LXC, closes the file descriptor used by the TAP device, 
		 * and destroys the LXC. (Note) Outgoing Thread should be stopped
		 */
		~LXC_Proxy();

		/*
		 * Creates an LXC by creating the appropriate bridge and TAP device. 
		 * Then the LXC is created. There is a 200 millisecond delay between 
		 * LXC Creation and launching
		 */
		void launchLXC();


		//---------------------------------------------------------------------
		//           Auxiliary information about TAP, LXC, Bridge
		//---------------------------------------------------------------------

		unsigned int intlxcIP;                    // IP address of host (and also the LXC)
		int          fd;                          // file descriptor
		string       Nhi;                         // NHI of the host
		void*        ptrToHost;                   // Pointer to host
		char         tapName[100];                // TODO: limits tapname to 100 characters
		char         lxcName[100];                // TODO: limits lxcName to 100 characters
		char         brName[100];                 // TODO: limits brName to 100 characters
		string       cmndToExec;                  // Single command to execute inside the LXC
		string 		 ttnProjectName;			  // Titan Project Name under which command was compiled
												  // It will be empty for INS-VT execution types.
		double	     relCPUSpeed;				  // Relative CPU Speed
		int			 eqTracerID;				  // Equivalent tracer ID
		bool		 isCompilerAssisted;		  // True if virtual time advancement is compiler assisted

		ltime_t      simulationStartSec;          // Absolute time when the LXC is frozen (seconds)
		ltime_t      simulationStartMicroSec;     // Absolute time when the LXC is frozen (microseconds)

		bool         commandSent;                 // Bool indicating whether a command was sent once
		ltime_t	     last_arrival_time;

		// Used only when isCompilerAssisted is True
		std::mutex pktsInTransitQueueMutex;		

		// Used only when isCompilerAssisted is True
		std::priority_queue< lPair, std::vector<lPair> ,
							std::greater<lPair> > pktsInTransit; 

	
		//---------------------------------------------------------------------
		// 			Functions for Modifying and Accessing Proxy
		//---------------------------------------------------------------------

		/*
		 * Prints out debug infor about the LXC Proxy
		 */
		void printInfo();

		/*
		 * Gets the elapsed virtual time since the simulation began.
		 */
		ltime_t getElapsedTime();


		void setEqTracerID(int tracerID);

		LxcManager* lxcMan;              // Pointer to the LXC Manager
		Timeline* timelineLXCAlignedOn;  // Timeline the LXC is aligned on

		//--------------------------------------------------------------------
		// 						Private Helper Functions
		//--------------------------------------------------------------------


		/*
		 * Creates a file descriptor to read from a TAP device. For more 
		 * details see the tutorial
		 * http://backreference.org/2010/03/26/tuntap-interface-tutorial/
		 */
		int tun_alloc(char *dev, int flags);

		/*
		 * Executes system command and retains the output.
		 */
		string exec_system_command(char* cmd);

		/*
		 * Executes the LXC command
		 */
		void exec_LXC_command(LxcCommand type);


		/*
		 *	Executed only if isCompilerAssisted is true
		 */
		void updateNextEarliestArrivalTime(int pktHash,
									   	   long long pktEarliestArrivalTime);


		/*
		 *	Used only when isCompilerAssisted is true
		 */
		long long getNextEarliestArrivalTime();
};

#endif
