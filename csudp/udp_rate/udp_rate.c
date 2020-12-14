#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <sys/time.h>

#define US_IN_MS 1000
#define MSG_SIZE 1000
#define BUFSIZE 1024


void udp_client(char * hostname, int portno, int rateMBps) {

  int sockfd, n;
	int serverlen;
	struct sockaddr_in serveraddr;
	struct hostent *server;
	char buf[BUFSIZE];
	struct timeval startTimeStamp;
	long startTS = 0;
  long targetEndTS = 0;
  long targetBytesSent = 0;
  long sendTS = 0;
  long bytesSent  = 0;
  long totalBytesSent = 0;
  int numMBs = 0;


	/* socket: create the socket */
	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockfd < 0) 
	  error("ERROR opening socket");

	/* gethostbyname: get the server's DNS entry */
	server = gethostbyname(hostname);
	if (server == NULL) {
    fprintf(stderr,"ERROR, no such host as %s\n", hostname);
    exit(0);
	}

	/* build the server's Internet address */
	bzero((char *) &serveraddr, sizeof(serveraddr));
	serveraddr.sin_family = AF_INET;
	bcopy((char *)server->h_addr, 
	  (char *)&serveraddr.sin_addr.s_addr, server->h_length);
	serveraddr.sin_port = htons(portno);

	/* get a message from the user */

	int cc = 0;
	printf("UDP Client Started !. Sleeping for 100ms\n");
	printf("UDP Client resumed from sleep\n");
	
  memset(buf, 0, BUFSIZE);
  for (int i = 0; i < MSG_SIZE; i++) {
    buf[i] = 'a';
  }

	while(1) {
		/* send the message to the server */

    if (!startTS) {
      gettimeofday(&startTimeStamp, NULL);
    	startTS = startTimeStamp.tv_sec * 1000000 + startTimeStamp.tv_usec;
      bytesSent = 0;

      targetBytesSent = rateMBps; // number of bytes to send per us

      // rate limit every 10ms
      targetEndTS = startTS + 10*US_IN_MS;

      // multiply by number of us in target interval
      targetBytesSent = targetBytesSent * (targetEndTS - startTS);      

    }

    struct timeval sendTimeStamp,JAS_Timestamp;
    gettimeofday(&sendTimeStamp, NULL);
    sendTS = sendTimeStamp.tv_sec * 1000000 + sendTimeStamp.tv_usec;
		serverlen = sizeof(serveraddr);
		n = sendto(sockfd, buf, strlen(buf), 0, &serveraddr, serverlen);
    bytesSent += n;

    totalBytesSent += n;

    if (sendTS >= targetEndTS) {
      startTS = 0;
    } else if (bytesSent >= targetBytesSent) {
      long timeLeft = targetEndTS - sendTS;
      usleep(timeLeft);
    }

    if (totalBytesSent >= 1000000) {
      numMBs ++;
      totalBytesSent = 0;
      printf("Client sent: %d MBs of data\n", numMBs);
    }
  }
}
void udp_server(char * hostname, int portno, int rateMBps) {
  int sockfd; /* socket */
  int clientlen; /* byte size of client's address */
  struct sockaddr_in serveraddr; /* server's addr */
  struct sockaddr_in clientaddr; /* client addr */
  struct hostent *hostp; /* client host info */
  char buf[BUFSIZE]; /* message buf */
  char *hostaddrp; /* dotted decimal host addr string */
  int optval; /* flag value for setsockopt */
  int n; /* message byte size */

  long bytesReceived = 0;
  int numMBs = 0;
  
  /* 
   * socket: create the parent socket 
   */
  sockfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (sockfd < 0) 
    error("ERROR opening socket");

  /* setsockopt: Handy debugging trick that lets 
   * us rerun the server immediately after we kill it; 
   * otherwise we have to wait about 20 secs. 
   * Eliminates "ERROR on binding: Address already in use" error. 
   */
  optval = 1;
  setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, 
	     (const void *)&optval , sizeof(int));

  /*
   * build the server's Internet address
   */
  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
  serveraddr.sin_port = htons((unsigned short)portno);

  /* 
   * bind: associate the parent socket with a port 
   */
  if (bind(sockfd, (struct sockaddr *) &serveraddr, 
	   sizeof(serveraddr)) < 0) 
    error("ERROR on binding");

  /* 
   * main loop: wait for a datagram, then echo it
   */
  int numReceived = 0;
  clientlen = sizeof(clientaddr);
  printf("UDP server started \n");
  while (1) {

    /*
     * recvfrom: receive a UDP datagram from a client
     */
    bzero(buf, BUFSIZE);
    n = recvfrom(sockfd, buf, BUFSIZE, 0,
		 (struct sockaddr *) &clientaddr, &clientlen);
    if (n < 0)
      error("ERROR in recvfrom");

    bytesReceived += n;

    if (bytesReceived >= 1000000) {
      numMBs ++;
      bytesReceived = 0;
      printf("Server received: %d MBs of data\n", numMBs);
    }
    
  }
}



int main(int argc, char** argv) {
    
    int numMessages;
    if (argc < 5) {
        printf ("Not enough args: ./udp_test [client or server] server_ip server_port rateMBps\n");
        exit(0);
    }

    numMessages = atoi(argv[4]);
    if (strcmp(argv[1], "client") == 0) {
        udp_client(argv[2], atoi(argv[3]), numMessages);
    } else {
        udp_server(argv[2], atoi(argv[3]), numMessages);
    }
    return 0;

}
