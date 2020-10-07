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


#include <unistd.h> 		// close
	

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

// Emu Packet Class - contains information about packet that is captured by 
// LXC Proxy Through a TAP device
class EmuPacket
{
	public:

		// packet length in bytes
		int     len;
		ltime_t outgoingTime;
		ltime_t incomingTime;

		u_short ethernetType;
		int     incomingFD;
		int     outgoingFD;

		 // packet payload pointer
		unsigned char *data;               

		// pointer to destProxy which should recv packet
		LXC_Proxy * destProxy;				

		// contructor
		EmuPacket(int len);  

		// destructor               
		virtual ~EmuPacket();  

		// generate an extra copy of this packet, for multicast             
		EmuPacket* duplicate();
};

class LXC_Proxy
{
	public:


		//! Constructor.
		// 1st Param - NHI of the S3FNet Host which will be emulated
		// 2nd Param - The IP address of the S3FNet Host that will be emulated
		// Note: careful with changing the host/network order
		// 3rd Param - Pointer to the LXC Manager
		// 4th Param - Timeline this LXC is aligned on
		// TODO: 4th Param can be replaced with actual ID
		LXC_Proxy(string, unsigned int, LxcManager* c, Timeline* timeline);


		//! Destructor.
		// Stops an LXC, closes the file descriptor used by the TAP device, 
		// and destroys the LXC. (Note) Outgoing Thread should be stopped.
		~LXC_Proxy();

		
		// Creates an LXC by creating the appropriate bridge and TAP device. 
		// Then the LXC is created. There is a 200 millisecond delay between 
		// LXC Creation and launching.
		void launchLXC();

		// IP address of host (and also the LXC)
		unsigned int intlxcIP;   

		// file descriptor                 
		int          fd;                          

		// NHI of the host
		string       Nhi;                         

		// Pointer to host
		void*        ptrToHost;                   

		// TODO: limits tapname to 100 characters
		char         tapName[100];  

		// TODO: limits lxcName to 100 characters              
		char         lxcName[100];  

		// TODO: limits brName to 100 characters              
		char         brName[100];     

		// Single command to execute inside the LXC            
		string       cmndToExec;                  
		

		// Titan Project Name under which command was compiled
		// It will be empty if VirtualTimeManager is KRONOS.
		string 		 ttnProjectName;			  

		// Relative CPU Speed
		float	     relCPUSpeed;	

		// Equivalent tracer ID			  
		int			 eqTracerID;				  

		// Absolute time when the LXC is frozen (seconds)
		ltime_t      simulationStartSec;          

		// Absolute time when the LXC is frozen (microseconds)
		ltime_t      simulationStartMicroSec;     
                
		ltime_t	     last_arrival_time;

		// Used only when VirtualTimeManager is Titan
		std::mutex pktsInTransitQueueMutex;		

		// Used only when VirtualTimeManager is Titan
		std::priority_queue< lPair, std::vector<lPair> ,
							std::greater<lPair> > pktsInTransit; 

	
		
		//! Prints out debug infor about the LXC Proxy
		void printInfo();

		
		//! Gets the elapsed virtual time since the simulation began.
		ltime_t getElapsedTime();


		//! Sets tracerID for this proxy
		void setEqTracerID(int tracerID);

		// Pointer to the LXC Manager
		LxcManager* lxcMan;             

		// Timeline the LXC is aligned on 
		Timeline* timelineLXCAlignedOn;  

		
		
		// Creates a file descriptor to read from a TAP device. For more 
		// details see the tutorial
		// http://backreference.org/2010/03/26/tuntap-interface-tutorial/
		int tun_alloc(char *dev, int flags);

		
		// Executes system command and retains the output.
		string exec_system_command(char* cmd);

		
		// Executes the LXC command
		void exec_LXC_command(LxcCommand type);


		
		//	Useful only if VirtualTimeManager is TITAN
		void updateNextEarliestArrivalTime(int pktHash,
									   	   long long pktEarliestArrivalTime);


		
		//	Useful only when VirtualTimeManager is TITAN
		long long getNextEarliestArrivalTime();

		// Called when a packet is delivered to the LXC
		void signalPacketDelivery(int pktHash);

		// Returns true if any packets are in transit to the LXC
		bool arePktsInTransit();

		// Returns the IP and MAC address to be assigned to the LXC
		std::pair<string, string> getIPAndMacAddr();
};

#endif
