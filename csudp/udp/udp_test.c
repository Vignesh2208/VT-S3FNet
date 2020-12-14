#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <sys/time.h>
 

#define BUFSIZE 1024


void udp_client(char * hostname, int portno, int numMessages) {

  int sockfd, n;
	int serverlen;
	struct sockaddr_in serveraddr;
	struct hostent *server;
	char buf[BUFSIZE];
	struct timeval startTimeStamp;
	long startTS;


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
	gettimeofday(&startTimeStamp, NULL);
	startTS = startTimeStamp.tv_sec * 1000000 + startTimeStamp.tv_usec;

	while(1) {
		bzero(buf, BUFSIZE);
		/* send the message to the server */
		// For debugging SocketHook		
		struct timeval sendTimeStamp,JAS_Timestamp;
		gettimeofday(&sendTimeStamp, NULL);
		long sendTS = sendTimeStamp.tv_sec * 1000000 + sendTimeStamp.tv_usec;
		sprintf(buf, "%ld", sendTS);
		serverlen = sizeof(serveraddr);
		printf("Sending Ping SEQ: %d after: %ld us\n", cc, sendTS - startTS);
		n = sendto(sockfd, buf, strlen(buf), 0, &serveraddr, serverlen);
		
		/* print the server's reply */
		n = recvfrom(sockfd, buf, strlen(buf), 0, &serveraddr, &serverlen);
		struct timeval receiveTimestamp;
		gettimeofday(&receiveTimestamp, NULL);
		long recvTS = receiveTimestamp.tv_sec * 1000000 + receiveTimestamp.tv_usec;
		printf("reply received from server after: %ld us\n", recvTS - sendTS);
		if (n < 0) {
		  error("ERROR in recvfrom");
		}	

    usleep(10000);

    cc++;

    if (numMessages > 0 && cc >= numMessages)
      break;
	}
}
void udp_server(char * hostname, int portno, int numExpectedPings) {
  int sockfd; /* socket */
  int clientlen; /* byte size of client's address */
  struct sockaddr_in serveraddr; /* server's addr */
  struct sockaddr_in clientaddr; /* client addr */
  struct hostent *hostp; /* client host info */
  char buf[BUFSIZE]; /* message buf */
  char *hostaddrp; /* dotted decimal host addr string */
  int optval; /* flag value for setsockopt */
  int n; /* message byte size */
  
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
    long sendTS;
    long recvTS;
    char * eptr;

    struct timeval recvTimeStamp;
		gettimeofday(&recvTimeStamp, NULL);

		recvTS = recvTimeStamp.tv_sec * 1000000 + recvTimeStamp.tv_usec;

    /* Convert the provided value to a decimal long */
    sendTS = strtol(buf, &eptr, 10);
	  numReceived++;
	
    hostaddrp = inet_ntoa(clientaddr.sin_addr);
    if (hostaddrp == NULL)
      error("ERROR on inet_ntoa\n");

    printf("server received %d/%d. Rx - Tx (usec) = %ld\n", strlen(buf), n, recvTS - sendTS);
     
    n = sendto(sockfd, buf, strlen(buf), 0, 
	       (struct sockaddr *) &clientaddr, clientlen);
    if (n < 0) 
      error("ERROR in sendto");

    if (numExpectedPings > 0 && numReceived >= numExpectedPings)
      break;  
  }
}



int main(int argc, char** argv) {
    
    int numMessages;
    if (argc < 5) {
        printf ("Not enough args: ./udp_test [client or server] server_ip server_port\n");
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
