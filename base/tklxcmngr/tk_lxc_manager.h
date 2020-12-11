/**
 * \file tk_lxc_manager.h
 *
 * \brief LXC Manager
 *
 * authors : Vladimir Adam
 */

#ifndef __TIMEKEEPER_LXCMNGR_H__
#define __TIMEKEEPER_LXCMNGR_H__

#ifndef __S3F_H__
#error "tk_lxc_manager.h can only be included by s3f.h"
#endif

#include <sys/time.h>
#include "lxc_proxy.h"
#include <poll.h>
#include "../s3fnet-definitions.h"


#define PACKET_PARSE_SUCCESS        0
#define PACKET_PARSE_UNKNOWN_PACKET 1
#define PACKET_PARSE_IGNORE_PACKET  2
#define PARSE_PACKET_SUCCESS_IP	    3
#define PARSE_PACKET_SUCCESS_ARP    4

class LXC_Proxy;
class VirtualTimeManagerInterface;
class Graph;

#define START_LXCS 100
#define STOP_LXCS  200


enum VirtualTimeManagerType {
	KRONOS,
	TITAN,
	DEFAULT
};

class LxcManager
{
	public:

		//---------------------------------------------------------------------
		// 						Constructors / Destructor
		//---------------------------------------------------------------------

		// Initializes all member variables. Takes as Interface as paramater in
		// case it needs more information about the model
		LxcManager(Interface* inf);

		//! TODO: deallocate all necessary allocated memory
		~LxcManager();

		//! Return one instant of the LXC Manager (called in api/interface.cc)
		static LxcManager* get_lxc_manager(Interface* inf);

		//!
		// Initialize the directory that will contain logs after an 
		// experiment runs. Each run will be uniquely identified by a folder 
		// named with the number of seconds elapsed since epoch time.
		// Creates the log files by getting the log director from the DML 
		// file (see s3fnet/s3fnet.cc).
		//
		// First an instance of LXC Manager is created. As soon as a 
		// SimInterface is called (which creates an instance of LXC Manager, 
		// this function is called to finish initializing the LXC Manager before
		// S3FNet further parses the DML files and builds the model
		void init(char* outputDir,
			VirtualTimeManagerType vtManagerType, int isLookaheadEnabled);


		//! Returns true if the configured virtual time manager is titan
		bool IsVirtualTimeManagerTitan ();

		//! The thread which handles all incoming packets coming from LXCs
		pthread_t incomingThread;


		 // pointer to interface
		Interface* siminf;       


		// vector of all proxies maintained by the LXC Manager
		std::vector<std::vector<int>> dependantTimelines;   

		std::vector<ltime_t> dependantTlShortestDist;                                   
		
		// vector of all proxies maintained by the LXC Manager                                   
		std::vector<LXC_Proxy*> listOfProxies; 

		 // contains the list of Proxies by a timeline                      
		vector<LXC_Proxy*>** listOfProxiesByTimeline;               

		// vector where each element corresponds to a timeline and
		// how much total time a timeline called progress
		vector<long> vectorOfTotalTimesSpentAdvancing;               

		// vector where each element corresponds to a timeline and
		// the total times the LXC on it advanced
		vector<long> vectorOfHowManyTimesTimelineAdvanced;     
		// vector where each element corresponds to a timeline and
		// the total times this timeline called progress(...)
		vector<long> vectorOfHowManyTimesTimelineCalledProgress;  
		// flag to see if the thread responsible for capturing LXCS
		// is running
		bool isSimulatorRunning;   

		// Number of appointments made by each timeline
		vector<int> timelineNumAppts;

		// Number of simulated hosts in each timeline
		vector<int> timelineNumSimulatedHosts;

		vector<ltime_t> syncWindowEAts;

		// Set to 1 if lookahead computation is enabled
		int isLookaheadEnabled;

		// Used at global synchronization window to set earlies packet arrival times
		int numWaitingTimelines;

		// Max lookkahead possible to be set by any emulated timeline
		ltime_t maxLookaheadUs;

		// A lock to control setting earliest arrival times at global sync window
		pthread_mutex_t  setEatMutex;

		// path to the folder where information about each run will be stored                                  
		string  logFolder;

		// file pointer to the log file                                           
		FILE*   fpLogFile;

		// Graph linking all timelines and containing hosts and switches
		Graph * timelineGraph;

		// Total number of entities which are hosts
		int totalNumHosts;

		// Interface to handle virtual time manager operations
		VirtualTimeManagerInterface * vtManagerInterface = NULL;
		

		//!	Statistics Printing
		void printLXCstats();
		
		
		//! Contains the logic for the thread capturing LXC packets.
		void* manageIncomingPackets();

		// Attempt at parallelizing the LXC creation. Currently unused due to 
		// the fact that sometimes, the LXC may not be fully created before 
		// calling gettimePID which would result in a PID of -1.
		void* setUpTearDownLXCs(unsigned int timelineID, int type);

		
		//! Inserts the a LXC Proxy into to list for LXC Manager use
		void insertProxy(LXC_Proxy* p);

		
		// Returns the proxy that represents the LXC with a given IP address.
		// Used after parsing a packet so that when it injected from a host 
		// with IP address.
		LXC_Proxy* findDestProxy(unsigned int dstIP);

		
		//! Advances LXCs on a given timeline to the absolute time timeToAdvance
		void advanceLXCsOnTimeline(unsigned int id, ltime_t timeToAdvance);

		//! Starts all LXCs and calls SynchronizeAndFreeze
		void syncUpLXCs();

		
		//! Returns pointer to proxy with specified nhi ID
		LXC_Proxy* getLXCProxyWithNHI(string nhi);

		//----------------------------------------------------------------
		// 				Simulation Management
		//----------------------------------------------------------------

		
		// Calls StopExp() which cleans up the experiment. 
		// It also unfreezes all the LXCs. At this point, it is safe
		// to rmmod the TimeKeeper module
		void stopExperiment();

		
		// Subroutine inside manageIncomingPackets(...) which is called each 
		// tiem a poll(...) function returns. Depending on the
		// file descriptor that has data ready to be read, this function, 
		// parses the packet from a particular LXC and injects
		// it into the simulation.
		void handleIncomingPacket(vector<LXC_Proxy*>* proxiesToCheck);

	
		
		//! Helper function which sets up the log files
		void setupLog();

		
		// For each timeline in the simulation, this function prints out what 
		// LXCs are aligned on that timeline
		void printInfoAboutHashTable();

		
		// Prints the content of a captured packet. Useful for analysis. 
		// I recommend http://sadjad.me/phd/ and use that online tool
		// to quickly decode packets
		string print_packet(char* pkt_ptr, int len);

		
		// Analyzes a given packet and decides whether this packet should be 
		// ignored. For instance, an IPv6 packet is ignored
		std::pair<int, unsigned int> analyzePacket(char* pkt_ptr, int len,
												   u_short* etherType);

		//! Reads from file descriptor that goes through a TAP device
		int cread (int fd, char *buf, int n);

		//! Writes to a file descriptor that goes through a TAP device
		int cwrite(int fd, char *buf, int n);


		//! Prints into the log files fpLogFile and standard out
		void debugPrint(char* format, ...);

		//! Prints into the log files fpLogFile
		void debugPrintFileOnly(char* format, ...);

		//! Returns the total number of microsecond since epoch time
		unsigned long getWallClockTime();


		//! Returns a hash of the packet contents
		std::pair<int, unsigned int> packet_hash(char * s,int size);


		int readAndProcessNxtPacket(LXC_Proxy * proxy, char * buffer);

		//! Sets host ids for all nodes in a subnet starting from the given
		//  number.
		void setHostGraphNodeIDs(void * subnet, int* startIDNumber);

		//! called by composeTimelineGraph to recursively process and add nodes
		//  in a subnet to the global timeline graph
		void processHostsInAllSubNets(void * subnet); 

		//! Recursively processes all nets and constructs a timeline graph
		void composeTimelineGraph(void * topNet);

		//! Computes the minimum lookahead among all proxies aligned on src timeline
		//  w.r.t to any entity aligned on dest timeline
		ltime_t getProxiesLookahead(int src_tl, int dest_tl);


		//! Computes nearest distance between a host and any host/router aligned on dest_tl
		ltime_t getHostLookahead(void * ptrToHost, int dst_tl);

		//! Returns true if there are no simulated hosts on this timeline
		bool isTimelineFullyEmulated(int timelineID);

		//! Returns true if lookahead is enabled
		bool isVtLookaheadEnabled() { return isLookaheadEnabled == 1; }

		//! Returns true if any packets are in transit to the specified timeline
		bool arePktsInTransit(int tl);

		//! Called at global sync window to set earliest arrival times
		void SetEatSyncWindow();

		ltime_t getTimelineSmallestInTranstTime(int timelineID);

		long long getTimelineExclEat(int timelineID);




};

typedef struct threadInfo {
	LxcManager*  lxcManager;
	unsigned int timelineID;

} threadInfo;

typedef struct launchThreadInfo {
	LxcManager*  lxcManager;
	unsigned int timelineID;
	int typeFlag;

} launchThreadInfo;

#endif
