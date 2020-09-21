/* 
 * udpclient.c - A simple UDP client
 * usage: udpclient <host> <port>
 */
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

/* 
 * error - wrapper for perror
 */
void error(char *msg) {
    perror(msg);
    exit(0);
}

int main(int argc, char **argv) {
	int sockfd, portno, n;
	int serverlen;
	struct sockaddr_in serveraddr;
	struct hostent *server;
	char *hostname;
	char buf[BUFSIZE];
	struct timeval startTimeStamp;
	long startTS;

	/* check command line arguments */
	if (argc != 4) {
		fprintf(stderr,"usage: %s <hostname> <port> <numMessages>\n", argv[0]);
		exit(0);
	}

	int numMessages = atoi(argv[3]);

	hostname = argv[1];
	portno = atoi(argv[2]);

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
	usleep(100000);
	printf("UDP Client resumed from sleep\n");

	gettimeofday(&startTimeStamp, NULL);
	startTS = startTimeStamp.tv_sec * 1000000 + startTimeStamp.tv_usec;

	for (cc = 0; cc < numMessages; cc++)
	{
		bzero(buf, BUFSIZE);
		sprintf(buf, "Ping SEQ %.4d", cc);

		/* send the message to the server */

		// For debugging SocketHook		
		struct timeval sendTimeStamp,JAS_Timestamp;
		gettimeofday(&sendTimeStamp, NULL);
		
		long sendTS = sendTimeStamp.tv_sec * 1000000 + sendTimeStamp.tv_usec;

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
	}

	return 0;
}
