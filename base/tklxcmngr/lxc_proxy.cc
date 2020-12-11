/**
 * \file lxc_proxy.cc
 *
 * \brief LXC Proxy
 *
 * authors : Vladimir Adam
 */

#include <arpa/inet.h>
#include <s3f.h>
#include <sstream>
#include <iomanip>

#include <s3fnet/src/net/host.h>
#include <algorithm>

#include <errno.h>
#include <sys/mman.h>
#include <sys/shm.h>
#include <sys/time.h>

#include <sys/socket.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#include <sys/ioctl.h>		// ioctl


#include "graph_utils.h"
#include "virtual_time_manager.h"

#ifdef ENABLED_VT_MANAGER_TITAN
extern "C" {
	#include <VT_functions.h>
}
#else
extern "C" {
	#include <Kronos_functions.h>
}
#endif
extern "C" void ns_2_timeval(s64 currTstamp, struct timeval * tv);

//----------------------------------------------------------------------------
// 					Emu Packet Class
//----------------------------------------------------------------------------

EmuPacket::EmuPacket(int len)
{
	this->len = len;
	data = new unsigned char[len];
	outgoingTime = -1;
	incomingTime = -1;
	incomingFD   = -1;
	outgoingFD   = -1;
	ethernetType = 0;
	dest_emu_tl = -1;
	eat = 0;
	pktNumber = 0;
	destProxy = NULL;
}

EmuPacket::~EmuPacket() {
	if (data) delete data;
}

EmuPacket* EmuPacket::duplicate() {
	EmuPacket* ppkt = new EmuPacket(len);
	memcpy(ppkt->data, data, len);
	ppkt->incomingTime = incomingTime;
	ppkt->outgoingTime = outgoingTime;
	ppkt->ethernetType = ethernetType;
	ppkt->incomingFD   = incomingFD;
	ppkt->outgoingFD   = outgoingFD;
	ppkt->destProxy = destProxy;
	ppkt->pktNumber = pktNumber;
	ppkt->eat = eat;
	ppkt->dest_emu_tl = dest_emu_tl;
	assert(ppkt->len == len);
	printf("Duplicate called\n");
	exit(0);
	return ppkt;
}

//----------------------------------------------------------------------------------------------------------------------
// 												LXC Proxy Class
//----------------------------------------------------------------------------------------------------------------------

LXC_Proxy::LXC_Proxy(string nhiID, unsigned int ipAddress, LxcManager* lm,
					Timeline* timel) {


	assert(lm    != NULL);
	assert(timel != NULL);

	Nhi                  = nhiID;
	intlxcIP             = ipAddress;
	lxcMan               = lm;
	timelineLXCAlignedOn = timel;
	fd                   = -1;
	ptrToHost            = NULL;
	cmndToExec           = "echo 'no command sent to LXC'";
	eqTracerID			 = -1;
	pktIDCounter		 =  0;

	// Initialize the TAP Name, LXC Name, and Bridge Name
	string tempTap = "tap" + Nhi;
	std::replace( tempTap.begin(), tempTap.end(), ':', '-');
	strcpy(tapName, tempTap.c_str());
	string tempLXC = "lxc" + Nhi;
	std::replace( tempLXC.begin(), tempLXC.end(), ':', '-');
	strcpy(lxcName,tempLXC.c_str());
	string tempBr = "br-" + Nhi;
	std::replace( tempBr.begin(), tempBr.end(), ':', '-');
	strcpy(brName,tempBr.c_str());

	last_arrival_time = 0;
	
	lxcMan->debugPrint("LXC proxy initialization: %s successfull\n",lxcName);


}

std::pair<string, string> LXC_Proxy::getIPAndMacAddr() {
	char buffer[20];
	memset(buffer, 0, 20);
	unsigned int convertedIP = htonl(intlxcIP);
	const char* result = inet_ntop(AF_INET, &convertedIP, buffer,
								   sizeof(buffer));
	std::string myIP = string(result);
	std::stringstream stream;
	stream << std::hex << eqTracerID;
	std::string myMacHex( stream.str() );
	std::string myMac = "";

	while (myMacHex.length() != 12)
		myMacHex += "0";

	for (int i = 0; i < myMacHex.length(); i++) {
		myMac += myMacHex[i];
		if (i % 2 == 1 && i != myMacHex.length() - 1)
			myMac += ":";
	}
	return std::pair<std::string, std::string>(myIP, myMac);
}

void LXC_Proxy::setEqTracerID(int tracerID) {
	assert(tracerID > 0);
	this->eqTracerID = tracerID;
}

void LXC_Proxy::launchLXC() {
	exec_LXC_command(LxcCommand::LXC_CREATE);
	usleep(TIME_200_MS_IN_US);
	exec_LXC_command(LxcCommand::LXC_START_TRACER);
}


LXC_Proxy::~LXC_Proxy() {

	close(fd);
	cout << "Stopping LXC Proxy. Tracer-ID: " << eqTracerID << endl;
	//exec_LXC_command(LXC_STOP);
	exec_LXC_command(LXC_DESTROY);
	cout << "Stopped LXC Proxy. Tracer-ID: " << eqTracerID << endl;
}

void LXC_Proxy::printInfo() {
	/*char buffer[20];
	unsigned int convertedIP = htonl(intlxcIP);
	const char* result = inet_ntop(AF_INET, &convertedIP, buffer,
								  sizeof(buffer));*/

	std::pair<std::string, std::string> res = getIPAndMacAddr();

	lxcMan->debugPrint("|==========================\n");
	lxcMan->debugPrint("| NHI     : %s \n", Nhi.c_str());
	lxcMan->debugPrint("| LXC     : %s \n", lxcName);
	lxcMan->debugPrint("| Tap     : %s \n", tapName);
	lxcMan->debugPrint("| Bridge  : %s \n", brName);
	lxcMan->debugPrint("| IP      : %u (%s) \n", intlxcIP, res.first.c_str());
	lxcMan->debugPrint("| MAC     : (%s) \n", res.second.c_str());
	lxcMan->debugPrint("| FD      : %d\n",  fd);
	lxcMan->debugPrint("| Command : %s\n", cmndToExec.c_str());
	lxcMan->debugPrint("|==========================\n");
}

// Gets the elapsed time from the LXC by asking the timekeeper to issue a
// system call to the process with the given PID (which refers to the LXC)
ltime_t LXC_Proxy::getElapsedTime() {
	struct timeval incomingPacketTimestamp;
	ns_2_timeval(
		this->lxcMan->vtManagerInterface->GetCurrentVirtualTimeTracer(eqTracerID),
		&incomingPacketTimestamp);
	assert(incomingPacketTimestamp.tv_sec >= simulationStartSec);
	long secElapsed = incomingPacketTimestamp.tv_sec  - simulationStartSec;
	long microSecElapsed 
		= incomingPacketTimestamp.tv_usec - simulationStartMicroSec;
	long elapsedMicroSec = secElapsed * 1000000 +  microSecElapsed;
	return elapsedMicroSec;
}

int LXC_Proxy::tun_alloc(char *dev, int flags) {

	struct ifreq ifr;
	int fd, err;
	char *clonedev = "/dev/net/tun";

	/* Arguments taken by the function:
	*
	* char *dev: the name of an interface (or '\0'). MUST have enough
	*   space to hold the interface name if '\0' is passed
	* int flags: interface flags (eg, IFF_TUN etc.)
	*/

	/* open the clone device */
	if( (fd = open(clonedev, O_RDWR)) < 0 ) {
		printf("Open Clone Device Success\n");
		return fd;
	}

	/* preparation of the struct ifr, of type "struct ifreq" */
	memset(&ifr, 0, sizeof(ifr));

	ifr.ifr_flags = flags;   /* IFF_TUN or IFF_TAP, plus maybe IFF_NO_PI */

	if (*dev) {
	 /* if a device name was specified, put it in the structure; otherwise,
	  * the kernel will try to allocate the "next" device of the
	  * specified type */
	 strncpy(ifr.ifr_name, dev, IFNAMSIZ);
	} else {
		perror("Dev Not Working\n");
	}


	/* try to create the device */
	if( (err = ioctl(fd, TUNSETIFF, (void *) &ifr)) < 0 ) {
		printf("Error Opening Device\n");
		close(fd);
		return err;
	}

	/* if the operation was successful, write back the name of the
	* interface to the variable "dev", so the caller can know
	* it. Note that the caller MUST reserve space in *dev (see calling
	* code below) */
	strcpy(dev, ifr.ifr_name);

	/* this is the special file descriptor that the caller will use to talk
	* with the virtual interface */
	return fd;
}

string LXC_Proxy::exec_system_command(char* cmd) {
    // see
	// http://stackoverflow.com/questions/478898/how-to-execute-a-command-and-get-output-of-command-within-c

	FILE* pipe = popen(cmd, "r");
    if (!pipe){
		printf("exec system command Error!\n");
 		return "ERROR";
	}

    char buffer[128];
    std::string result = "";
    while(!feof(pipe)) {
    	if(fgets(buffer, 128, pipe) != NULL)
    		result += buffer;
    }
    pclose(pipe);
    //cout<< " Result = "<<result<<endl;

    return result;
}

void LXC_Proxy::exec_LXC_command(LxcCommand type) {
	string cmd = "";
	char config[200];
	char buffer[20];
	memset(config, 0, 200);
	/*unsigned int convertedIP = htonl(intlxcIP);
	const char* result = inet_ntop(AF_INET, &convertedIP, buffer,
									sizeof(buffer));*/
	std::pair<string, string> res = getIPAndMacAddr();
	string bridge = " " + string(brName);
	string tap    = " " + string(tapName);
	string lxc    = " " + string(lxcName);
	string ipAddr = " " + string(res.first);
	string macAddr = " " + string(res.second);

	sprintf(config, " %s/lxc-scripts/lxc-config/%u",
			PATH_TO_S3FNETLXC, timelineLXCAlignedOn->s3fid());

	switch(type)
	{
		case LXC_CREATE:
			printf("Called lxc create\n");
			cmd = string(PATH_TO_S3FNETLXC) + string("/lxc-scripts/create") 
				+ tap + ipAddr + macAddr + bridge + lxc + string(config);

			// Open up a TAP DEVICE since our LXC is already created
			fd = tun_alloc(tapName, IFF_TAP | IFF_NO_PI);
			assert(fd > 0);

			usleep(TIME_100_MS_IN_US);
			break;

		case LXC_STOP:
			cmd = "lxc-stop -n "  + lxc;
			break;

		case LXC_DESTROY:
			cmd = string(PATH_TO_S3FNETLXC) + string("/lxc-scripts/destroy") 
					+ tap + bridge + lxc;
			break;

		case LXC_START_TRACER:
			cmd = this->lxcMan->vtManagerInterface->GetEncalsulatedTracerCommand(
				eqTracerID, timelineLXCAlignedOn->s3fid(), relCPUSpeed,
				ttnProjectName, cmndToExec, ipAddr);
			
			std::cout << "Tracer: " << eqTracerID << " Encapsulated CMD = " << cmd << std::endl; 
			cmd = "lxc-start -n" + lxc + " -d " + " -f" + string(config) + " -- " + cmd;
			break;
		
		default:
			std::cout << "Unknown LXC command.... Exiting\n";
			exit(1);
	}

	cout << "Executing LXC command = "<< cmd << "\n";
	exec_system_command((char*)cmd.c_str());
}



void LXC_Proxy::updateNextEarliestArrivalTime(int pktHash,
									   	  	  s64 pktEarliestArrivalTime) {
	pktsInTransitQueueMutex.lock();
	pktsInTransit.push(std::make_pair(pktEarliestArrivalTime, pktHash));
	pktsInTransitQueueMutex.unlock();
}

void LXC_Proxy::signalPacketDelivery(int pktHash) {

	std::vector<lPair> tmpVector;
	pktsInTransitQueueMutex.lock();
	while(!pktsInTransit.empty()) {
		int topHash = pktsInTransit.top().second;
		if(topHash == pktHash) {
			pktsInTransit.pop();
			break;
		} else {
			s64 topPktEAT = pktsInTransit.top().first;
			topHash = pktsInTransit.top().second;
			pktsInTransit.pop();
			tmpVector.push_back(std::make_pair(topPktEAT, topHash));			
		}
	}

	for (int i = 0; i < (int)tmpVector.size(); i++) {
		pktsInTransit.push(std::make_pair(
			tmpVector[i].first, tmpVector[i].second));
	}
	pktsInTransitQueueMutex.unlock();

}


s64 LXC_Proxy::getNextEarliestArrivalTime(bool safe) {

	s64 eat;
	s64 currTimestamp = this->lxcMan->vtManagerInterface->GetCurrentVirtualTimeTracer(eqTracerID);
	 
	s64 nearestDepTimelineDistNs = 
		(this->lxcMan->dependantTlShortestDist[timelineLXCAlignedOn->s3fid()] * NS_IN_USEC);
	/*s64 nearestHostDistNs
		= (s64)(lxcMan->timelineGraph->getNearestHostDist(
			((s3f::s3fnet::Host *)ptrToHost)->getGraphNodeID()) * NS_IN_USEC); */
	//std::cout << "Nearest Host Dist Secs = " << nearestHostDistsecs << " Host = " 
	//		  << ((s3f::s3fnet::Host *)ptrToHost)->getGraphNodeID() <<"\n";
	s64 eatIfNoPktsInQueue = currTimestamp + nearestDepTimelineDistNs;

	assert(eatIfNoPktsInQueue >= currTimestamp); 
	pktsInTransitQueueMutex.lock();
	if (pktsInTransit.empty())
		eat = eatIfNoPktsInQueue;
	else {
		eat = pktsInTransit.top().first;
		if (eat > eatIfNoPktsInQueue && safe) {
			eat = eatIfNoPktsInQueue; // we are being safe here
		} else if (eat < currTimestamp) {
			eat = currTimestamp;
		}
	}
	pktsInTransitQueueMutex.unlock();

	if (!this->lxcMan->IsVirtualTimeManagerTitan())
		return currTimestamp;

	assert(eat >= currTimestamp);
	return eat;
}

s64 LXC_Proxy::getSmallestInTransitTime() {
	s64 eat; 
	pktsInTransitQueueMutex.lock();
	if (pktsInTransit.empty())
		eat = 0;
	else {
		eat = pktsInTransit.top().first;
	}
	pktsInTransitQueueMutex.unlock();
	return eat;
}


bool LXC_Proxy::arePktsInTransit() {
	bool inTransit = false;
	pktsInTransitQueueMutex.lock();
	if (!pktsInTransit.empty())
		inTransit = true;
	pktsInTransitQueueMutex.unlock();
	return inTransit;
}

