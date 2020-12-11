/**
 * \file lxcemu_message.cc
 * \brief Source file for the LxcEmuMessage class. Adapted from dummy_message.cc
 *
 * authors : Vladimir Adam
 */


#include "os/lxcemu/lxcemu_message.h"

#define PACKET_SIZE 1600

namespace s3f {
namespace s3fnet {

S3FNET_REGISTER_MESSAGE(LxcemuMessage, S3FNET_PROTOCOL_TYPE_LXCEMU);

LxcemuMessage::LxcemuMessage()
{
	ppkt = NULL;
}

LxcemuMessage::LxcemuMessage(const LxcemuMessage& msg) :
  ProtocolMessage(msg)
{
	EmuPacket* original = msg.ppkt;
	ppkt = original->duplicate();
	printf("LXCMessage Unplanned Copy Constructor");
	assert(false);

}

LxcemuMessage::~LxcemuMessage(){}

int LxcemuMessage::packingSize()
{
  // must add the parent class packing size
  int mysiz = ProtocolMessage::packingSize();

  assert(false);

  return mysiz + sizeof(EmuPacket*);
}

int LxcemuMessage::realByteCount()
{
	assert(ppkt != NULL);
	assert(ppkt->ethernetType != 0);

	int realBytes = 0;

	// TODO:Double check this since S3FNet apparently does not take
	// first 14 bytes when calculating transmission time.
	switch(ppkt->ethernetType)
	{
		case 0x0800:	// IP
			realBytes = ppkt->len - 20 - 14 - 14;
			break;
		case 0x0806: // ARP
			realBytes = 8; // since s3f does not count MAC during transmission, ARP packet = 42 bytes - 14 = 28
			// since we are simulating IP layer, = 28. This is so that S3FNet thinks the packet is 42 bytes
			break;
		default:
			fprintf(stderr, "LxcEmuMessage::realByteCount() - unhandled ethernet type\n");
			assert(false);
	}

	assert(realBytes >= 0);
	return realBytes;
}

void LxcemuMessage::erase_all() {
	
	assert(this->ppkt->destProxy != NULL && this->ppkt->len <= PACKET_SIZE);

	//memcpy(pkt_copy, this->ppkt->data, this->ppkt->len);
	//std::pair<int, unsigned int> res 
	//	= this->ppkt->destProxy->lxcMan->packet_hash((char *)this->ppkt->data, this->ppkt->len);
	//int pktHash = res.first;

	//printf("Signalling packet delivery at: Proxy: %d for pktHash: %d\n", 
	//		this->ppkt->destProxy->eqTracerID, pktHash);
	
	this->ppkt->destProxy->signalPacketDelivery(this->ppkt->pktNumber);
	delete this->ppkt;
	ProtocolMessage::erase_all();
}

}; // namespace s3fnet
}; // namespace s3f
