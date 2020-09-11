/**
 * \file tk_lxc_manager.cc
 *
 * \brief LXC Manager
 *
 * authors : Vladimir Adam
 */

#include "pktheader.h"
#include <s3f.h>
#include <string.h>

#include <sstream>
#include <iomanip>

#include <s3fnet/src/net/host.h>
#include <s3fnet/src/net/net.h>
#include <s3fnet/src/net/link.h>
#include <s3fnet/src/net/network_interface.h>
#include <s3fnet/src/util/shstl.h>
#include <algorithm>

#include <errno.h>
#include <arpa/inet.h>
#include <netinet/ip_icmp.h>
#include <netinet/udp.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <fstream>
#include <cstdarg>

#include "graph_utils.h"

extern "C" 
{
	#include <VT_functions.h>   
	
}

#define ETHER_TYPE_IP    (0x0800)
#define ETHER_TYPE_ARP   (0x0806)
#define ETHER_TYPE_8021Q (0x8100)
#define ETHER_TYPE_IPV6  (0x86DD)
#define PACKET_SIZE 1600

extern "C" void ns_2_timeval(s64 currTstamp, struct timeval * tv);

/*
void print_ip(unsigned int ip)
{
    unsigned char bytes[4];
    bytes[0] = ip & 0xFF;
    bytes[1] = (ip >> 8) & 0xFF;
    bytes[2] = (ip >> 16) & 0xFF;
    bytes[3] = (ip >> 24) & 0xFF;   
    printf("%d.%d.%d.%d\n", bytes[3], bytes[2], bytes[1], bytes[0]);        
}*/


//----------------------------------------------------------------------------
// 			LXC Manager Class Functions
//----------------------------------------------------------------------------



LxcManager::LxcManager(Interface* inf)
{

	siminf = inf;
	isSimulatorRunning      = false;
	listOfProxiesByTimeline = NULL;
	fpLogFile               = NULL;
	incomingThread = -1;
}


void LxcManager::setHostGraphNodeIDs(void * net,
									 int* startIDNumber) {

	if (!net || !startIDNumber)
		return;

	s3f::s3fnet::Net * subnet = (s3f::s3fnet::Net *)net;

	s3f::s3fnet::S3FNET_INT2PTR_MAP& hosts = subnet->getHosts();
	s3f::s3fnet::S3FNET_INT2PTR_MAP& nets = subnet->getNets();

	for(unsigned i=0; i < hosts.size(); i++) {
		s3f::s3fnet::Host * currHost = (s3f::s3fnet::Host *)hosts[i];
		assert(currHost->getGraphNodeID() == -1);

		if (currHost->isRouter())
			std::cout << "Setting graphNodeID: " << *startIDNumber << " to switch: " << std::endl;
		else
			std::cout << "Setting graphNodeID: " << *startIDNumber << " to host:  " << std::endl;
		std::cout << "Net details: " << std::endl;
		subnet->display();
		std::cout << std::endl;

		std::cout << "Host/Switch details: " << std::endl;
		currHost->display();
		std::cout << std::endl;

		currHost->setGraphNodeID(*startIDNumber);
		*startIDNumber = *startIDNumber + 1;
	}

	for(s3f::s3fnet::S3FNET_INT2PTR_MAP::iterator iter = nets.begin();
		iter != nets.end(); iter++) {
		s3f::s3fnet::Net* nextNet = (s3f::s3fnet::Net*)(iter->second);

		if (nextNet)
			setHostGraphNodeIDs(nextNet, startIDNumber);
  	} 
}


void LxcManager::processHostsInAllSubNets(void * net) {

	if (!net)
		return;

	s3f::s3fnet::Net * subnet = (s3f::s3fnet::Net *)net;
	s3f::s3fnet::S3FNET_POINTER_VECTOR& links = subnet->getLinks();
	s3f::s3fnet::S3FNET_INT2PTR_MAP& nets = subnet->getNets();

	for(unsigned i=0; i < links.size(); i++) {
		s3f::s3fnet::Link* pLink = (s3f::s3fnet::Link*)links[i];
		vector<s3f::s3fnet::NetworkInterface*> ifaces 
				= pLink->getNetworkInterfaces();
		for(unsigned j = 0; j < ifaces.size(); j++) {
			s3f::s3fnet::Host * attachedHost1 = ifaces[j]->getHost();

			assert(attachedHost1->getGraphNodeID() >= 0);
			for(unsigned k = 0; k < ifaces.size(); k++) {
				if (k == j)
					continue;
				s3f::s3fnet::Host * attachedHost2 = ifaces[k]->getHost();
				assert(attachedHost2->getGraphNodeID() >= 0);
				timelineGraph->addEdge(
					attachedHost1->getGraphNodeID(),
					attachedHost1->inNet()->getAlignedTimelineID(),
					attachedHost2->getGraphNodeID(),
					attachedHost2->inNet()->getAlignedTimelineID(),
					pLink->getDelay(),
					attachedHost1->isRouter(),
					attachedHost2->isRouter());
			}
			
		}
	}


	for(s3f::s3fnet::S3FNET_INT2PTR_MAP::iterator iter = nets.begin();
		iter != nets.end(); iter++) {
		s3f::s3fnet::Net* nextNet = (s3f::s3fnet::Net*)(iter->second);

		if (nextNet)
			processHostsInAllSubNets(nextNet);
  	} 
}

void LxcManager::composeTimelineGraph(void * net) {

	if (!net)
		return;

	s3f::s3fnet::Net * top_net = (s3f::s3fnet::Net * )net;
	int numHosts = 0;
	setHostGraphNodeIDs(top_net, &numHosts);
	if (numHosts) {
		timelineGraph = new Graph(numHosts, siminf->get_numTimelines());
		processHostsInAllSubNets(top_net);
		timelineGraph->populateAllShortestPaths();
	}

	this->totalNumHosts = numHosts;
}

void LxcManager::init(char* outputDir)
{
	struct timeval runTimestamp;
	gettimeofday(&runTimestamp, NULL);
	std::stringstream temp;
	temp << outputDir << "/" << runTimestamp.tv_sec;
	logFolder = temp.str();
	setupLog();

	// Initialize hash table of LXC proxies for quick lookup!
	unsigned int numTimelines = siminf->get_numTimelines();

	debugPrint("|==================================================\n");
	debugPrint("| LXC Manager Created\n");
	debugPrint("| Simulation has %d timelines\n", numTimelines);
	debugPrint("|==================================================\n");

	listOfProxiesByTimeline = new vector<LXC_Proxy*>*[numTimelines];
	for (unsigned int i = 0; i < numTimelines; i++) {
		listOfProxiesByTimeline[i] = new vector<LXC_Proxy*>();
		vectorOfTotalTimesSpentAdvancing.push_back(0);
		vectorOfHowManyTimesTimelineAdvanced.push_back(0);
		vectorOfHowManyTimesTimelineCalledProgress.push_back(0);
	}

	assert(vectorOfTotalTimesSpentAdvancing.size() == numTimelines);
}


LxcManager::~LxcManager() {
	delete timelineGraph;
}

//----------------------------------------------------------------------------------------------------------------------
// 												Thread Functions
//----------------------------------------------------------------------------------------------------------------------

void* LxcManager::setUpTearDownLXCs(unsigned int timelineID, int typeFlag)
{
	vector<LXC_Proxy*>* proxiesOnTimeline = listOfProxiesByTimeline[timelineID];

	assert(typeFlag == START_LXCS || typeFlag == STOP_LXCS );

	for (unsigned int i = 0; i < proxiesOnTimeline->size(); i++)
	{
		LXC_Proxy* proxyOnTimeline = (*proxiesOnTimeline)[i];
		assert(proxyOnTimeline->timelineLXCAlignedOn->s3fid() == timelineID);

		if (typeFlag == START_LXCS) {
			proxyOnTimeline->launchLXC();
			printf("[%u] Creating %s ", timelineID, proxyOnTimeline->lxcName);
		} else {
			cout << timelineID << " Deleting " << proxyOnTimeline->lxcName << "\n";
			proxyOnTimeline->exec_LXC_command(LXC_STOP);
			close(proxyOnTimeline->fd);
			proxyOnTimeline->exec_LXC_command(LXC_DESTROY);
		}
	}
	return (void*)NULL;
}


int LxcManager::readAndProcessNxtPacket(LXC_Proxy * proxy, char * buffer) {
	int incomingFD = proxy->fd;
	u_short ethT = 0;
	ltime_t arrivalTime = 0;
	assert(incomingFD > 0);
	memset(buffer, 0, PACKET_SIZE);

	int nread = cread(incomingFD, buffer, PACKET_SIZE);

	if (nread <= 0)
		return 0;

	std::pair<int, unsigned int> res = analyzePacket(buffer, nread, &ethT);
	unsigned int destIP = res.second;
	int packet_status   = res.first;
    int payload_hash = 0, payload_len = 0;
	int numConsumedBytes = 0;

	if (packet_status == PACKET_PARSE_IGNORE_PACKET
	    || packet_status ==  PACKET_PARSE_UNKNOWN_PACKET) {
		return 0;
	}

	struct timeval incomingPacketTimestamp;
	s64 incomingPacketTimeNS;


	res = packet_hash(buffer, nread);
	payload_hash = res.first;
	payload_len = res.second;
	
	if (packet_status == PARSE_PACKET_SUCCESS_IP) {
		
		printf("Detected IP payload hash: %d, payload_len: %d\n", payload_hash, payload_len);
		numConsumedBytes = payload_len;

		if (!payload_hash) {
			incomingPacketTimeNS = GetCurrentTimeTracer(proxy->eqTracerID);
			arrivalTime = proxy->getElapsedTime();
		} else {

			incomingPacketTimeNS = GetPktSendTimeAPI(proxy->eqTracerID,
			      									 payload_hash);
			ns_2_timeval(incomingPacketTimeNS, &incomingPacketTimestamp);

			long secElapsed 
				= incomingPacketTimestamp.tv_sec - proxy->simulationStartSec;
			long microSecElapsed 
				= incomingPacketTimestamp.tv_usec - proxy->simulationStartMicroSec;
			arrivalTime = secElapsed * 1000000 +  microSecElapsed;
		}
	} else {
		numConsumedBytes = 0;
		incomingPacketTimeNS = GetCurrentTimeTracer(proxy->eqTracerID);
		arrivalTime = proxy->getElapsedTime();
	}

	proxy->last_arrival_time = arrivalTime;
	struct in_addr ip_addr;
	ip_addr.s_addr = destIP;
	
	LXC_Proxy* destinationProxy = findDestProxy(destIP);
	if (destinationProxy == NULL) {
		printf("Dropping packet intended for destIP: %s: "
			   "No one to give it to !\n", inet_ntoa(ip_addr));
		cout << print_packet(buffer, nread);	
	}
	else {

		EmuPacket* pkt = new EmuPacket(nread);
		memcpy(pkt->data, buffer, nread);
		pkt->incomingFD   = incomingFD;
		pkt->outgoingFD   = destinationProxy->fd;
		pkt->incomingTime = arrivalTime;
		pkt->ethernetType = ethT;
		pkt->destProxy = destinationProxy;

		assert(pkt->incomingFD != pkt->outgoingFD);

		s3f::s3fnet::Host* srcHost 
			= (s3f::s3fnet::Host*)proxy->ptrToHost;

		s3f::s3fnet::Host* dstHost 
			= (s3f::s3fnet::Host*)destinationProxy->ptrToHost;

		s64 shortestDistNS = (timelineGraph->getShortestDist(
								srcHost->getGraphNodeID(),
								dstHost->getGraphNodeID()) * NSEC_PER_SEC);
		

		srcHost->inNet()->getTopNet()->injectEmuEvent(
			srcHost, pkt, destIP);
		destinationProxy->updateNextEarliestArrivalTime(payload_hash,
			incomingPacketTimeNS + shortestDistNS);
	}
	return numConsumedBytes;
}

void LxcManager::handleAllEnqueuedPackets(vector<LXC_Proxy*>* proxiesToCheck) {
	//struct pollfd ufds[proxiesToCheck->size()];
	//int ret = 0;
	char buffer[PACKET_SIZE];
	for (unsigned int i = 0; i < proxiesToCheck->size(); i++) {
		LXC_Proxy* proxy = (*proxiesToCheck)[i];
		
		int numEnqueuedBytes = get_num_enqueued_bytes(proxy->eqTracerID);
		int numDequeuedBytes = 0;
		
		if (numEnqueuedBytes <= 0)
			continue;

		printf("Num Enqueued Bytes is positive and = %d\n", numEnqueuedBytes);
		while (numDequeuedBytes < numEnqueuedBytes) {
			// there is some data which will become available shortly
			numDequeuedBytes += readAndProcessNxtPacket(proxy, buffer);
		}
		
	}


}



//----------------------------------------------------------------------------
// 					Other Functions
//----------------------------------------------------------------------------

void LxcManager::handleIncomingPacket(vector<LXC_Proxy*>* proxiesToCheck) {


	struct pollfd ufds[proxiesToCheck->size()];
	int ret = 0;
	char buffer[PACKET_SIZE];

	//handleAllEnqueuedPackets(proxiesToCheck);

	// handle anything left-over
	do {
		
		for (unsigned int i = 0; i < proxiesToCheck->size(); i++) {
			LXC_Proxy* proxy = (*proxiesToCheck)[i];
			ufds[i].fd = proxy->fd;
			ufds[i].events  = POLLIN;
			ufds[i].revents = 0;
		}
		ret = poll(ufds, proxiesToCheck->size(), 0);

		if (ret <= 0)
			break;
		
		// find out to see which FD got something
		for (unsigned int i = 0; i < proxiesToCheck->size(); i++) {
			LXC_Proxy* proxy = (*proxiesToCheck)[i];
			if(ufds[i].revents & POLLIN) {
				readAndProcessNxtPacket(proxy, buffer);
			}
		}

	} while (ret > 0); // end of do-while
	
}

LXC_Proxy* LxcManager::findDestProxy(unsigned int dstIP) {
	for (unsigned int i = 0; i < listOfProxies.size(); i++) {
		LXC_Proxy* potentialDestinationProxy = listOfProxies[i];
		if (potentialDestinationProxy->intlxcIP == dstIP) {
			return potentialDestinationProxy;
		}
	}
	return NULL;
}

LxcManager* LxcManager::get_lxc_manager(Interface* inf) {
	LxcManager* controller = new LxcManager(inf);
	return controller;
}

void LxcManager::syncUpLXCs() {

	long lxcTimestampSec;
	long lxcTimestampMicroSec;
	int numTimelines, numTracers;
	struct timeval tv_lxcTimestamp;

	printInfoAboutHashTable();

	numTimelines = siminf->get_numTimelines();
	numTracers = listOfProxies.size();
	debugPrint("|==================================================\n");
	debugPrint("| Initializing VT experiment                     \n");
	debugPrint("|==================================================\n\n");

	InitializeVtExp(EXP_CS, numTimelines, numTracers);

	debugPrint("|==================================================\n");
	debugPrint("| Creating and Launching LXCs                      \n");
	debugPrint("|==================================================\n\n");


	for (unsigned int i = 0; i < listOfProxies.size(); i++) {
		LXC_Proxy* proxy = listOfProxies[i];
		proxy->setEqTracerID(i + 1);
		proxy->launchLXC();
	}

	sleep(1);


	debugPrint("|==================================================\n");
	debugPrint("| Calling SynchronizeAndFreeze. Syncing up LXCs\n");
	debugPrint("|==================================================\n\n");

	if (listOfProxies.size() != 0)
		SynchronizeAndFreeze();

	for (unsigned int i = 0; i < listOfProxies.size(); i++) {
		LXC_Proxy* proxy = listOfProxies[i];
		ns_2_timeval(GetCurrentTimeTracer(proxy->eqTracerID),
					&tv_lxcTimestamp);
		lxcTimestampSec      = tv_lxcTimestamp.tv_sec;
		lxcTimestampMicroSec = tv_lxcTimestamp.tv_usec;
		proxy->simulationStartSec      = lxcTimestampSec;
		proxy->simulationStartMicroSec = lxcTimestampMicroSec;

		debugPrint("| %s Frozen at [ %ld sec %ld usec ]\n", proxy->lxcName,
					lxcTimestampSec, lxcTimestampMicroSec);
	}
	debugPrint("\n|==================================================\n");

}

void LxcManager::insertProxy(LXC_Proxy* p) {
	int timelineID = p->timelineLXCAlignedOn->s3fid();
	assert(timelineID >= 0 && timelineID < (int)siminf->get_numTimelines());
	listOfProxiesByTimeline[timelineID]->push_back(p);
	listOfProxies.push_back(p);
}

void LxcManager::printLXCstats() {

	#ifdef LOGGING
	for (unsigned int i = 0; i < listOfProxies.size(); i++) {
		string cmd  = "cp " +  string(PATH_TO_S3FNETLXC) + "/data/" 
			+ string(listOfProxies[i]->lxcName) + " " + logFolder ;
		system(cmd.c_str());
	}
	#endif

	unsigned int nT = siminf->get_numTimelines();

	debugPrint(
		"\n|============================================================|\n");
	double totalSecondSpentAdvancing = 0;

	for (unsigned int ii = 0; ii < nT; ii++) {
		double seconds = vectorOfTotalTimesSpentAdvancing[ii] / 1e6;
		totalSecondSpentAdvancing += seconds;
		debugPrint(
			"| Timeline %d called Progress %ld times "
			"for a total of %f seconds\n",
			ii, vectorOfHowManyTimesTimelineCalledProgress[ii], seconds);
	}

	debugPrint(
		"|============================================================|\n");
	debugPrint("| Cumulative emulation seconds %f\n",
				totalSecondSpentAdvancing);
	debugPrint("| Simulation run time is %g seconds\n",
				siminf->sim_exc_time()/1e6);
	debugPrint("| Total run time is %g seconds\n",
				siminf->full_exc_time()/1e6);
	debugPrint(
		"|============================================================|\n");
}
ltime_t getProxiesLookahead(int srcTimelineID, int destTimelineID) {
	vector<LXC_Proxy*>* proxiesOnTimeline = listOfProxiesByTimeline[srcTimelineID];

	if (proxiesOnTimeline->size() == 0)
		return 0;

	ltime_t min_lookahead = -1;
	ltime_t curr_lookahead = 0;
	for (unsigned int i = 0; i < proxiesOnTimeline->size(); i++) {
		LXC_Proxy* proxyOnTimeline = (*proxiesOnTimeline)[i];
		Host * proxyHost = proxyOnTimeline->ptrToHost;
		assert(proxyHost);
		curr_lookahead = 
			GetTracerLookahead(proxyOnTimeline->eqTracerID) + 
			(timelineGraph->getNearestTimelineDist(proxyHost->getGraphNodeID(),
				destTimelineID) * NSEC_PER_SEC);
		if (min_lookahead == -1 || min_lookahead > curr_lookahead)
			min_lookahead = curr_lookahead;
	}
	min_lookahead = min_lookahead > 0 ? min_lookahead : 0;
	return min_lookahead;

}
void LxcManager::advanceLXCsOnTimeline(unsigned int timelineID,
				       				   ltime_t timeToAdvanceTo) {
	// Keep track of how many LXCs need to be advanced

	vector<LXC_Proxy*> proxiesBeingAdvanced;
	vector<LXC_Proxy*>* proxiesOnTimeline = listOfProxiesByTimeline[timelineID];

	// this timeline does not have any proxies - don't advance it
	if (proxiesOnTimeline->size() == 0) {
		debugPrint("Timeline has no proxies !\n");
		return;
	}
	
	
	ltime_t lxc_actual_vt          = (*proxiesOnTimeline)[0]->getElapsedTime(); // all lxcs will be frozen at same time. so just get one.
	ltime_t desired_vt             = timeToAdvanceTo;
	ltime_t time_needed_to_advance_us = desired_vt - lxc_actual_vt;
	ltime_t min_lookahead = -1;
	ltimt_t curr_lookahead;

	if (desired_vt <= lxc_actual_vt && next_make_appt_tl)
		return;

	vectorOfHowManyTimesTimelineCalledProgress[timelineID]++;

	//if (vectorOfHowManyTimesTimelineCalledProgress[timelineID] < 100)
	debugPrint("|----------- Advancing Timeline: %d by %llu (us). timeToAdvanceTo: %llu (us). ElapsedTime: %llu (us) -----------|\n",
		    timelineID, time_needed_to_advance_us, timeToAdvanceTo, lxc_actual_vt);

	

	if (time_needed_to_advance_us <= 0)
		return;

	for (unsigned int i = 0; i < proxiesOnTimeline->size(); i++) {
		LXC_Proxy* proxyOnTimeline = (*proxiesOnTimeline)[i];

		// set eat here. This could be used by emulated processes when they run
		// this round.
		SetEarliestArrivalTime(proxyOnTimeline->eqTracerID,
							   proxyOnTimeline->getNextEarliestArrivalTime());
	}

	

	unsigned long startTime = getWallClockTime();
	ProgressTimelineBy((int)timelineID, time_needed_to_advance_us*1000);
	unsigned long finishTime = getWallClockTime();


	handleIncomingPacket(proxiesOnTimeline);

	return;
}

LXC_Proxy* LxcManager::getLXCProxyWithNHI(string nhi)
{
	for (unsigned int i = 0; i < listOfProxies.size(); i++) {
		LXC_Proxy* potentialDestinationProxy = listOfProxies[i];
		if (potentialDestinationProxy->Nhi.compare(nhi) == 0) {
			return potentialDestinationProxy;
		}
	}
	printf("Attempted to get proxy of NHI (%s), that doesn't exist - please "
		   "fix DML file\n", nhi.c_str());
	exit(0);
	return NULL;
}

//-------------------------------------------------------------------------------------------------------
// 										Helper Methods
//-------------------------------------------------------------------------------------------------------

void LxcManager::printInfoAboutHashTable() {
	//debugPrint("|==================================================\n");
	for (unsigned int i = 0; i < siminf->get_numTimelines(); i++)
	{
		vector<LXC_Proxy*>* proxies = listOfProxiesByTimeline[i];
		debugPrint(" ____________________________________________\n");
		debugPrint("|\n");
		debugPrint("| Printing out Info about Timeline %ld ...\n", i);
		debugPrint("|_____\n");
		if ((int)proxies->size() == 0)
			debugPrint("      | Timeline %d has has no LXC proxies\n", i);

		for (int j = 0; j < (int)proxies->size(); j++)
		{
			LXC_Proxy* prx = (*proxies)[j];
			debugPrint("      | Timeline %d has Proxy LXC %s\n", i,
						prx->lxcName);
		}
		debugPrint("      |______________________________________\n");
	}
}

std::pair<int, unsigned int> LxcManager::analyzePacket(char* pkt_ptr, int len,
						       u_short* ethT) {
	assert(ethT != NULL);
	sniff_ethernet* ether = (sniff_ethernet*)pkt_ptr;
	u_short ether_type    = ntohs(ether->ether_type);
	
	int ether_offset     = 0;
	int dstIPAddr_offset = 0, srcIPAddr_offset = 0;
	int parse_packet_type = PARSE_PACKET_SUCCESS_IP;
	int is_udp = 0, is_tcp = 0, is_icmp = 0;

	struct icmphdr* tk_icmp_hdr;
	struct iphdr* tk_ip_header;
	struct udphdr* tk_udp_header;
	struct tcphdr* tk_tcp_header;

	char* ptrToDstIPAddr;
	char * ptrToSrcIPAddr;

	unsigned int dstIP, srcIP;

	u_short udp_src_port;
	(*ethT) = ether_type;

	switch(ether_type) {
		case ETHER_TYPE_IP:
			ether_offset = 14;
			dstIPAddr_offset = 16;
			srcIPAddr_offset = 12;

			// These statements deal with a packet that is sent out when an LXC is started as a DAEMON.
			// It try to send out some sort DHCP/ Bootstrap protocol to get an IP address (or something)
			// We ignore this packet and do not send it through the simulator.
			tk_ip_header = (struct iphdr*)(pkt_ptr + ether_offset);
			tk_ip_header = (struct iphdr*)(pkt_ptr + ether_offset);
			if (tk_ip_header->protocol == 0x11)	// UDP
			{
				tk_udp_header = (struct udphdr*)(pkt_ptr + ether_offset + tk_ip_header->ihl*4);
				udp_src_port = ntohs(tk_udp_header->source);
				is_udp = 1;
				
				if (udp_src_port == 68)
					return pair<int, unsigned int>(PACKET_PARSE_IGNORE_PACKET, -1);
			}
			if (tk_ip_header->protocol == 0x06)	// TCP
			{
				is_tcp = 1;
				tk_tcp_header = (struct tcphdr*)(pkt_ptr + ether_offset 
												+ tk_ip_header->ihl*4);
				

			}

			if (tk_up_header->protocol == 0x01) //ICMP
			{
				is_icmp = 1;
				tk_icmp_header = (struct icmphdr *)(pkt_ptr + ether_offset
													+ tk_ip_header->ihl*4);
			}
			parse_packet_type = PARSE_PACKET_SUCCESS_IP;
			break;

		case ETHER_TYPE_8021Q:
			ether_offset = 18;
			assert(false);
			parse_packet_type = PACKET_PARSE_IGNORE_PACKET;
			break;

		case ETHER_TYPE_ARP:
			ether_offset = 14;
			dstIPAddr_offset = 24;
			srcIPAddr_offset = 14;
			parse_packet_type = PARSE_PACKET_SUCCESS_ARP;
			break;

		case ETHER_TYPE_IPV6:
			return pair<int, unsigned int>(PACKET_PARSE_IGNORE_PACKET, -1);
			break;

		default:
			fprintf(stderr, "Unknown ethernet type, %04x %d, skipping...\n",
					ether_type, ether_type );
			cout << print_packet(pkt_ptr, len);
			assert(false);
			parse_packet_type = PACKET_PARSE_IGNORE_PACKET;
			break;
	}

	if (parse_packet_type == PARSE_PACKET_SUCCESS_IP) {
	 	
	 	dstIP = tk_ip_header->daddr;
		srcIP = tk_ip_header->saddr;

	} else {

		ptrToDstIPAddr = (pkt_ptr + ether_offset + dstIPAddr_offset);
		dstIP = *(unsigned int*)(ptrToDstIPAddr);

		ptrToSrcIPAddr = (pkt_ptr + ether_offset + srcIPAddr_offset);
		srcIP = *(unsigned int*)(ptrToSrcIPAddr);
	}

	char buffer[20];
	const char* result=inet_ntop(AF_INET, &dstIP,buffer,sizeof(buffer));
	char buffer_2[20];
	const char* result_2 = inet_ntop(AF_INET, &srcIP,buffer_2,sizeof(buffer_2));


	if(is_tcp){
		debugPrint("######################################\n");
		debugPrint("\n~~~~~~~~~~~~~~~~~~TCP :	");
		debugPrint("Ether Type: 0x%.4x\n", ether_type);
		debugPrint("Src IP string: %s\n",result_2);
		debugPrint("Dest IP string: %s\n", result);

		debugPrint("TCP source port : %d\n", tk_tcp_header->source);
		debugPrint("TCP dest port : %d\n", tk_tcp_header->dest);
		debugPrint("TCP seq : %d\n", tk_tcp_header->seq);
		debugPrint("TCP ack_seq : %d\n", tk_tcp_header->ack_seq);

		
		debugPrint("TCP syn : %d\n", tk_tcp_header->syn);
		debugPrint("TCP ack : %d\n", tk_tcp_header->ack);
		debugPrint("TCP rst : %d\n", tk_tcp_header->rst);
		debugPrint("TCP urg : %d\n", tk_tcp_header->urg);
		debugPrint("TCP fin : %d\n", tk_tcp_header->fin);
		debugPrint("TCP window : %d\n", tk_tcp_header->window);
		debugPrint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
	


	}

	if(is_udp){
		debugPrint("######################################\n");
		debugPrint("\n~~~~~~~~~~~~~~~~~~UDP :	");
		debugPrint("Ether Type: 0x%.4x\n", ether_type);
		debugPrint("Src IP string: %s\n",result_2);
		debugPrint("Dest IP string: %s\n", result);
		debugPrint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
	}

	if (is_icmp) {
		debugPrint("######################################\n");
		debugPrint("\n~~~~~~~~~~~~~~~~~~ICMP :	");
		debugPrint("Ether Type: 0x%.4x\n", ether_type);
		debugPrint("Src IP string: %s\n",result_2);
		debugPrint("Dest IP string: %s\n", result);
		debugPrint("ICMP Message Type: %d\n", tk_icmp_header->type);
		debugPrint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
	}

	if(!is_tcp && !is_udp && !is_icmp){

		debugPrint("######################################\n");
		if(parse_packet_type == PARSE_PACKET_SUCCESS_ARP)
			debugPrint("~~~~~~~~~~~~~~~~ARP~~~~~~~~~~~~~~~~~~\n");
		else {
			debugPrint("~~~~~~~~~~~~~~~~UNKNOWN~~~~~~~~~~~~~~~~~~\n");
		}

		debugPrint("Ether Type: 0x%.4x\n", ether_type);
		if (parse_packet_type == PARSE_PACKET_SUCCESS_IP) {
			debugPrint("IP Protocol Number: %d\n", tk_ip_header->protocol); 
		}
		debugPrint("Src IP string: %s\n",result_2);
		debugPrint("Dest IP string: %s\n", result);
		debugPrint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");		

	}

	assert(dstIP > 0);
	return pair<int, unsigned int>(parse_packet_type, ntohl(dstIP));
}

string LxcManager::print_packet(char* pkt_ptr, int len) {
	std::stringstream ss;
	ss << "Packet: ";
	for (int i = 0; i < len; i++)
	{
	    ss << hex << setw(2) << setfill('0') << (int)(unsigned char)pkt_ptr[i] 
		   << " ";
	}
	ss << "\n\n";
	return ss.str();
}

int LxcManager::cread(int fd, char *buf, int n) {
	int nread;
	if ((nread = read(fd, buf, n)) < 0) {
		perror("Reading data");
		exit(1);
	}
	return nread;
}

int LxcManager::cwrite(int fd, char *buf, int n) {
	int nwrite;
	if((nwrite=write(fd, buf, n)) < 0) {
	  perror("Writing data");
	  exit(1);
	}
	return nwrite;
}


void LxcManager::stopExperiment() {
	for (unsigned int i = 0; i < siminf->get_numTimelines(); i++) {
		vector<LXC_Proxy*>* proxies = listOfProxiesByTimeline[i];

		double totalMicroseconds = 0;

		for (int j = 0; j < (int)proxies->size(); j++) {
			LXC_Proxy* prx = (*proxies)[j];
			long startTime 
				= prx->simulationStartSec * 1e6 + prx->simulationStartMicroSec;
			long endTime   = startTime + prx->getElapsedTime();
			totalMicroseconds += (endTime - startTime);
		}

		debugPrint("Timeline %ld advanced its LXCs by %f seconds\n",
					i, totalMicroseconds/1000000.0);

	}

	debugPrint("|==================================================\n");
	debugPrint("| Calling STOP EXPERIMENT\n");
	debugPrint("|==================================================\n");
	StopExp();
}

void LxcManager::setupLog() {
	struct timeval runTimestamp;
	gettimeofday(&runTimestamp, NULL);

	// Make folder which will contain relevant debug files
	std::stringstream cmd_MakeLogDirSS;
	string cmd_MakeLogDir = string("mkdir -p ") + logFolder ;
	system(cmd_MakeLogDir.c_str());

	string logFile          = logFolder + "/log.txt";
	fpLogFile          = fopen(logFile.c_str(), "w" );
}

void LxcManager::debugPrint(char* format, ...) {
	// Print to Out File
	va_list argptr;
	va_start(argptr, format);
	vfprintf(fpLogFile, format, argptr);
	va_end(argptr);

	// Also print to STDOUT
	va_list temp;
	va_start(temp, format);
	vfprintf(stdout, format, temp);
	va_end(temp);
}

void LxcManager::debugPrintFileOnly(char* format, ...) {
	// Print to Out File
	va_list argptr;
	va_start(argptr, format);
	vfprintf(fpLogFile, format, argptr);
	va_end(argptr);
}

unsigned long LxcManager::getWallClockTime() {
	struct timeval tv;
	gettimeofday(&tv, 0);
	return (unsigned long)(tv.tv_sec * 1e6 + tv.tv_usec);
}

// for getting packet send time
std::pair<int, unsigned int> LxcManager::packet_hash(char * pkt,
													 int total_pkt_len) {

    int hash = 0;
    char * payload;
    int i = 0;
    int size = total_pkt_len;

    struct iphdr* ip_header;
    struct tcphdr * tcp_header;
	struct icmphdr * icmp_header;
    int ether_offset = sizeof(sniff_ethernet);
    int tcphdrlen, iphdrlen;

    ip_header = (struct iphdr*)(pkt + ether_offset);
    if (ip_header->protocol == 0x11) {
		// UDP
		iphdrlen = ip_header->ihl*sizeof (uint32_t);
		payload = (char *)(pkt + ether_offset 
							+ iphdrlen + sizeof(struct udphdr));
		size = total_pkt_len - (ether_offset 
								+ iphdrlen + sizeof(struct udphdr));

    } else if (ip_header->protocol == 0x6) {
		// TCP
		iphdrlen = ip_header->ihl*sizeof (uint32_t);
		tcp_header = (struct tcphdr *)(pkt + ether_offset + iphdrlen);
		tcphdrlen = sizeof (uint32_t) * tcp_header->doff;
		payload = (char *)(pkt + ether_offset + iphdrlen + tcphdrlen);
		size = total_pkt_len - (ether_offset + iphdrlen + tcphdrlen);

    } else if(ip_header->protocol == 0x01) { 
		// ICMP

		iphdrlen = ip_header->ihl*sizeof (uint32_t);
		payload = (char *)(pkt + ether_offset + iphdrlen 
							+ sizeof(struct icmphdr));
		size = total_pkt_len - (ether_offset 
								+ iphdrlen + sizeof(struct icmphdr));
	
	} else {
		return pair<int, unsigned int>(0, total_pkt_len);
    }
    
    for(i = 0; i < size; i++) {
    	hash += *payload;
    	hash += (hash << 10);
    	hash ^= (hash >> 6);
        ++payload;
    }

    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash << 15);

    if (hash < 0)
    	hash = -1 * hash;

    return pair<int, unsigned int>(hash, size);
}

