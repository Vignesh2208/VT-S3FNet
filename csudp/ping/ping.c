/* myping.c
 *
 * Copyright (c) 2000 Sean Walton and Macmillan Publishers.  Use may be in
 * whole or in part in accordance to the General Public License (GPL).
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
*/

/*****************************************************************************/
/*** myping.c                                                              ***/
/***                                                                       ***/
/*** Use the ICMP protocol to request "echo" from destination.             ***/
/*****************************************************************************/

#include <fcntl.h>
#include <errno.h>
#include <sys/socket.h>
#include <resolv.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/ip_icmp.h>
 #include <arpa/inet.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <strings.h>
#include <getopt.h>
#include <sys/time.h>
#include<sys/wait.h>

#define PACKETSIZE	64
struct packet
{
	struct icmphdr hdr;
	char msg[PACKETSIZE-sizeof(struct icmphdr)];
};

int pid=-1;
struct protoent *proto=NULL;

/*--------------------------------------------------------------------*/
/*--- checksum - standard 1s complement checksum                   ---*/
/*--------------------------------------------------------------------*/
unsigned short checksum(void *b, int len)
{	unsigned short *buf = b;
	unsigned int sum=0;
	unsigned short result;

	//printf("Finding checksum !\n");
	for ( sum = 0; len > 1; len -= 2 )
		sum += *buf++;
	if ( len == 1 )
		sum += *(unsigned char*)buf;
	sum = (sum >> 16) + (sum & 0xFFFF);
	sum += (sum >> 16);
	result = ~sum;
	return result;
}

/*--------------------------------------------------------------------*/
/*--- display - present echo info                                  ---*/
/*--------------------------------------------------------------------*/
int display(void *buf, int bytes)
{	int i;
	struct iphdr *ip = buf;
	struct icmphdr *icmp = buf+ip->ihl*4;

	unsigned int srcIP = ip->saddr;
	unsigned int dstIP = ip->daddr;
	int payload_size;
	long recvTS, sendTS;
	struct timeval recvTstamp;
	char * ptr;

	char buffer_1[20];
	const char* srcIPStr = inet_ntop(AF_INET, &srcIP, buffer_1, sizeof(buffer_1));
        payload_size = bytes - ip->ihl*4;

	if (ip->ttl != 255 && icmp->type != ICMP_ECHO) {
		gettimeofday(&recvTstamp, NULL);
		recvTS = recvTstamp.tv_sec * 1000000 + recvTstamp.tv_usec;
		char * payload = (buf + ip->ihl*4 + sizeof(struct icmphdr));
		sendTS = strtol(payload, &ptr, 10);
		printf("%d bytes from: %s: icmp_type = %d icmp_seq = %d ttl = %d time = %f ms\n",
			payload_size, srcIPStr, icmp->type, icmp->un.echo.sequence, ip->ttl, (float)(recvTS - sendTS)/1000.0);
                fflush(stdout);
		return 1;

	}
	return 0;

}

/*--------------------------------------------------------------------*/
/*--- listener - separate process to listen for and collect messages--*/
/*--------------------------------------------------------------------*/
void listener(int num_pings)
{	int sd, num_seen;
	struct sockaddr_in addr;
	unsigned char buf[1024];

	//sd = socket(PF_INET, SOCK_RAW, proto->p_proto);
	sd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
	if ( sd < 0 )
	{
		perror("socket");
		exit(0);
	}
	printf("Started listener !\n");
        fflush(stdout);
	num_seen = 0;
	int bytes = 0;
	for (;;)
	{	int len=sizeof(addr);
		bytes = 0;
		bzero(buf, 1024);
		bytes = recvfrom(sd, buf, 1024, 0, (struct sockaddr*)&addr, &len);
		if ( bytes > 0 ) {
			if (display(buf, bytes))
				num_seen ++;
		} else {
			perror("recvfrom");
		}
		if (num_seen >= num_pings && num_pings != -1)
			break;
	}
	return;
}

/*--------------------------------------------------------------------*/
/*--- ping - Create message and send it.                           ---*/
/*--------------------------------------------------------------------*/
void ping(struct sockaddr_in *addr, float ping_interval_secs, int num_pings)
{	const int val=64;
	int i, sd, cnt=1;
	struct packet pckt;
	struct sockaddr_in r_addr;
	long sendTS;
	struct timeval sendTstamp;

	//sd = socket(PF_INET, SOCK_RAW, proto->p_proto);
	sd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
	if ( sd < 0 )
	{
		perror("socket");
		return;
	}
	if ( setsockopt(sd, SOL_IP, IP_TTL, &val, sizeof(val)) != 0)
		perror("Set TTL option");
	if ( fcntl(sd, F_SETFL, O_NONBLOCK) != 0 )
		perror("Request nonblocking I/O");

	// waiting 100ms for listener to startup
	usleep(100000);
	for (;;)
	{	int len=sizeof(r_addr);

		//printf("Msg #%d\n", cnt);
		//recvfrom(sd, &pckt, sizeof(pckt), 0, (struct sockaddr*)&r_addr, &len);
		bzero(&pckt, sizeof(pckt));
		pckt.hdr.type = ICMP_ECHO;
		pckt.hdr.un.echo.id = pid;

		gettimeofday(&sendTstamp, NULL);
		sendTS = sendTstamp.tv_sec * 1000000 + sendTstamp.tv_usec;
		for ( i = 0; i < sizeof(pckt.msg); i++ )
			pckt.msg[i] = 0;
		sprintf(pckt.msg, "%lu", sendTS);
		pckt.hdr.un.echo.sequence = cnt;
		pckt.hdr.checksum = checksum(&pckt, sizeof(pckt));
		if ( sendto(sd, &pckt, sizeof(pckt), 0, (struct sockaddr*)addr, sizeof(*addr)) <= 0 )
			perror("sendto");
		cnt++;
		usleep((int)(ping_interval_secs*1000000));
		if (num_pings != -1 && cnt > num_pings) {
			//usleep(1000000);
			break;
		}
	}
}

/*--------------------------------------------------------------------*/
/*--- main - look up host and start ping processes.                ---*/
/*--------------------------------------------------------------------*/
int main(int argc, char *argv[])
{	struct hostent *hname;
	struct sockaddr_in addr;
	float ping_interval_secs = 1.0;
	int num_pings = -1;
	int option = 0;
	struct packet pckt;
	long sendTS;
	struct timeval sendTstamp;


	
	while ((option = getopt(argc, argv, "i:c:h")) != -1) {
		switch (option) {
		case 'i' : ping_interval_secs = atof(optarg);
			if (ping_interval_secs <= 0) {
				printf("ERROR: ping interval must be positive!\n");
				exit(0);
			}
			break;
		case 'c' : num_pings = atoi(optarg);
			if (num_pings <= 0) {
				printf("ERROR: num pings must be positive!\n");
				exit(0);
			}
			break;
		case 'h' :
		default: printf("usage: %s [-ic] <addr>\n Options:\n -i: interval in secs\n -c number of pings", argv[0]);
			exit(0);
		}
	}

	if ( argc < 2 )
	{
		printf("usage: %s [-ic] <addr>\n Options:\n -i: interval in secs\n -c number of pings", argv[0]);
		exit(0);
	}
	
	pid = getpid();
	proto = getprotobyname("ICMP");
	hname = gethostbyname(argv[argc - 1]);
	bzero(&addr, sizeof(addr));
	addr.sin_family = hname->h_addrtype;
	addr.sin_port = 0;
	addr.sin_addr.s_addr = *(long*)hname->h_addr;
	//printf("Num pings = %d, Ping interval: %f\n", num_pings, ping_interval_secs);
	if ( fork() == 0 )
		listener(num_pings);
	else {
		ping(&addr, ping_interval_secs, num_pings);
		wait(0);
	}
	
	return 0;
}

