#include <stdio.h> 
#include <unistd.h>
#include <netinet/in.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <sys/types.h> 
#include <sys/time.h>
#include <arpa/inet.h>
#include <netinet/tcp.h> 
#include <math.h>
#include <time.h>

#define US_IN_MS 1000
#define SND_BUF_SIZE 16384
#define RCV_BUF_SIZE 212992
#define MSG_SIZE 1460
#define DEFAULT_BURST_SIZE_KB 8
#define RATE_LIMIT_PERIOD_MS 10


double ran_expo(double lambda){
    double u;
    u = rand() / (RAND_MAX + 1.0);
    return -log(1- u) / lambda;
}


void tcp_client_poisson(char * server_ip, int server_port,
    int mean_interarrival_us, int burst_size_kb) {

  int clientSocket;
  int sndBufSize = SND_BUF_SIZE;
  int rcvBufSize = RCV_BUF_SIZE;
  char buffer[1500];
  struct sockaddr_in serverAddr;
  socklen_t addr_size;

  double lambda = (float)1e6 / (float)mean_interarrival_us;

  //usleep(100000);

  printf ("Client: MyPid: %d\n", getpid());
  clientSocket = socket(AF_INET, SOCK_STREAM, 0);
  printf ("Client socket fd = %d\n", clientSocket);
  fflush(stdout);

  if (sndBufSize > 0)
    setsockopt(clientSocket, SOL_SOCKET, SO_SNDBUF, &sndBufSize, sizeof(sndBufSize));

  if (rcvBufSize > 0)
    setsockopt(clientSocket, SOL_SOCKET, SO_RCVBUF, &rcvBufSize, sizeof(rcvBufSize));
  
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(server_port);
  serverAddr.sin_addr.s_addr = inet_addr(server_ip);
  memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);  

  
  addr_size = sizeof serverAddr;
  printf ("Connecting to server ...\n");
  connect(clientSocket, (struct sockaddr *) &serverAddr, addr_size);
  printf ("Sending data ...\n");
  fflush(stdout);

  memset(buffer, 0, MSG_SIZE + 10);
  for (int i = 0; i < MSG_SIZE; i++) {
    buffer[i] = 'a';
  }

  int msgLength = strlen(buffer);
  int numSent = 0;
  printf ("Sending msgs of size: %d to server ...\n", msgLength);
  int numBytesToSend = (burst_size_kb * 1024) / 8;
  
  while (1) {
        double sleep_period_secs = ran_expo(lambda);

        if (sleep_period_secs < 0.001) {
            // cap it at 1 ms
            sleep_period_secs = 0.001;
        }

        usleep((long)(sleep_period_secs * 1e6));
        numSent = 0;
        while (numSent < numBytesToSend) {
            int n = send(clientSocket,buffer,msgLength, 0);
            if (n < 0) {
                close(clientSocket);
                printf ("Finishing Client !\n");
                fflush(stdout);
                return;
            }
            numSent += n;
        }
        printf ("Sent: %d KB after: %f secs\n", burst_size_kb, sleep_period_secs);
        fflush(stdout);
        
  }

  fflush(stdout);
  close(clientSocket);   
}

void tcp_client_periodic(char * server_ip, int server_port,
    int period_us, int burst_size_kb) {

  int clientSocket;
  int sndBufSize = SND_BUF_SIZE;
  int rcvBufSize = RCV_BUF_SIZE;
  char buffer[1500];
  struct sockaddr_in serverAddr;
  socklen_t addr_size;

  //usleep(100000);

  printf ("Client: MyPid: %d\n", getpid());
  clientSocket = socket(AF_INET, SOCK_STREAM, 0);
  printf ("Client socket fd = %d\n", clientSocket);
  fflush(stdout);

  if (sndBufSize > 0)
    setsockopt(clientSocket, SOL_SOCKET, SO_SNDBUF, &sndBufSize, sizeof(sndBufSize));

  if (rcvBufSize > 0)
    setsockopt(clientSocket, SOL_SOCKET, SO_RCVBUF, &rcvBufSize, sizeof(rcvBufSize));
  
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(server_port);
  serverAddr.sin_addr.s_addr = inet_addr(server_ip);
  memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);  

  
  addr_size = sizeof serverAddr;
  printf ("Connecting to server ...\n");
  connect(clientSocket, (struct sockaddr *) &serverAddr, addr_size);
  printf ("Sending data ...\n");
  fflush(stdout);

  memset(buffer, 0, MSG_SIZE + 10);
  for (int i = 0; i < MSG_SIZE; i++) {
    buffer[i] = 'a';
  }

  int msgLength = strlen(buffer);
  int numSent = 0;
  printf ("Sending msgs of size: %d to server ...\n", msgLength);
  int numBytesToSend = (burst_size_kb * 1024) / 8;
  
  while (1) {
        numSent = 0;
        usleep(period_us);
        while (numSent < numBytesToSend) {
            int n = send(clientSocket,buffer,msgLength, 0);
            if (n < 0) {
                close(clientSocket);
                printf ("Finishing Client !\n");
                fflush(stdout);
                return;
            }
            numSent += n;
        }
        printf ("Sent: %d KB after: %d usecs\n", burst_size_kb, period_us);
        fflush(stdout);
  }

  close(clientSocket);
  printf ("Finishing Client !\n");
  fflush(stdout);  
}


void tcp_client_rate_limited(char * server_ip, int server_port, int rateMbps) {

    int sockfd, n;
	int serverlen;
	struct sockaddr_in serveraddr;
	struct hostent *server;
	char buffer[1500];
	struct timeval startTimeStamp;
	long startTS = 0;
    long targetEndTS = 0;
    long targetBytesSent = 0;
    long sendTS = 0;
    long bytesSent  = 0;
    long totalBytesSent = 0;
    int numMBs = 0;
    int clientSocket;
    int sndBufSize = SND_BUF_SIZE;
    int rcvBufSize = RCV_BUF_SIZE;
    struct sockaddr_in serverAddr;
    socklen_t addr_size;


    printf ("Client: MyPid: %d\n", getpid());
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    printf ("Client socket fd = %d\n", clientSocket);
    fflush(stdout);

    if (sndBufSize > 0)
    setsockopt(clientSocket, SOL_SOCKET, SO_SNDBUF, &sndBufSize, sizeof(sndBufSize));

    if (rcvBufSize > 0)
    setsockopt(clientSocket, SOL_SOCKET, SO_RCVBUF, &rcvBufSize, sizeof(rcvBufSize));

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(server_port);
    serverAddr.sin_addr.s_addr = inet_addr(server_ip);
    memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);  


    addr_size = sizeof serverAddr;
    printf ("Connecting to server ...\n");
    connect(clientSocket, (struct sockaddr *) &serverAddr, addr_size);
    printf ("Sending data ...\n");
    fflush(stdout);

    memset(buffer, 0, MSG_SIZE + 10);
    for (int i = 0; i < MSG_SIZE; i++) {
        buffer[i] = 'a';
    }

    int msgLength = strlen(buffer);
    int numSent = 0;
    int overShoot = 0;
    printf ("Sending msgs of size: %d to server at rate %d (Mbps)...\n", msgLength, rateMbps);

	while(1) {
		/* send the message to the server */

    if (!startTS) {
      gettimeofday(&startTimeStamp, NULL);
    	startTS = startTimeStamp.tv_sec * 1000000 + startTimeStamp.tv_usec;
      bytesSent = 0;

      targetBytesSent = (rateMbps * US_IN_MS) / 8; // number of bytes to send per ms

      // rate limit every 10ms
      targetEndTS = startTS + RATE_LIMIT_PERIOD_MS*US_IN_MS;

      // multiply by number of ms in target interval
      targetBytesSent = targetBytesSent * (RATE_LIMIT_PERIOD_MS);
      targetBytesSent -= overShoot;
      overShoot = 0;      
    }

    
    serverlen = sizeof(serveraddr);
    n = send(clientSocket,buffer,msgLength, 0);

    if (n < 0)
        break;
    struct timeval sendTimeStamp,JAS_Timestamp;
    gettimeofday(&sendTimeStamp, NULL);
    sendTS = sendTimeStamp.tv_sec * 1000000 + sendTimeStamp.tv_usec;

    bytesSent += n;
    totalBytesSent += n;


    if (sendTS >= targetEndTS) {
      startTS = 0;
      overShoot = 0;
    } else if (bytesSent >= targetBytesSent) {

      
      long timeLeft = targetEndTS - sendTS;
      overShoot = bytesSent - targetBytesSent;
      printf ("Bytes Sent = %d, targetBytesSent = %d, timeLeft (us) = %ld\n", bytesSent,
        targetBytesSent, timeLeft);
      fflush(stdout);
      startTS = 0;
      bytesSent = 0;
      usleep(timeLeft);
    }

    if (totalBytesSent >= 1000000) {
      numMBs ++;
      totalBytesSent = 0;
      printf("Client sent: %d MBs of data\n", numMBs);
    }
  }

  close(clientSocket);
  printf ("Finishing Client !\n");
  fflush(stdout);

}


void tcp_server(char * server_ip, int server_port) {

  int welcomeSocket, newSocket;
  char buffer[MSG_SIZE + 10];
  struct sockaddr_in serverAddr;
  struct sockaddr_storage serverStorage;
  //int ret;
  int sndBufSize = SND_BUF_SIZE;
  int rcvBufSize = RCV_BUF_SIZE;
  //char * finishMsg = "DONE";

  welcomeSocket = socket(AF_INET, SOCK_STREAM, 0);
  printf ("Server: MyPid: %d\n", getpid());
  printf ("Welcome socket fd = %d\n", welcomeSocket);

  if (sndBufSize > 0)
  setsockopt(welcomeSocket, SOL_SOCKET, SO_SNDBUF, &sndBufSize, sizeof(sndBufSize));

  if (rcvBufSize > 0)
  setsockopt(welcomeSocket, SOL_SOCKET, SO_RCVBUF, &rcvBufSize, sizeof(rcvBufSize));

  
  
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(server_port);
  serverAddr.sin_addr.s_addr = inet_addr(server_ip);
  memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);  

  printf ("Binding to server addr ...\n");
  bind(welcomeSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));

  printf ("Listening for new connections ...\n");
  if(listen(welcomeSocket, 5)==0)
    printf("Listening\n");
  else
    printf("Error\n");


  printf ("Accepting new connections ...\n");
  int len =  sizeof(serverStorage);
  newSocket = accept(welcomeSocket, (struct sockaddr *) &serverStorage, (socklen_t *)&len);

  if (sndBufSize > 0)
  setsockopt(newSocket, SOL_SOCKET, SO_SNDBUF, &sndBufSize, sizeof(sndBufSize));

  


  printf ("New Socket fd = %d\n", newSocket);
  memset(buffer, 0, MSG_SIZE + 10);
  for (int i = 0; i < MSG_SIZE; i++) {
    buffer[i] = 'a';
  }

  int msgLength = strlen(buffer);
  int numSent = 0;

  printf ("Sending msgs of size: %d to client ...\n", msgLength);
  struct timeval start, stop;
  int numChkPt = 0;
  int numMBs = 0;
  int n;
  int numReceived = 0;
  gettimeofday(&start, NULL);

  while (1) {
    n = recv(newSocket, buffer, 1500, 0);
    if (n < 0)
      break;
    numReceived += n;
    if (numReceived >= 1000000) {
      numMBs ++;
      numReceived = 0;
      printf("Server received: %d MBs of data\n", numMBs);
    }
    
  }
  
  gettimeofday(&stop, NULL);
  double time_taken = ((double)stop.tv_sec + (double)stop.tv_usec / 1e6 - ((double)start.tv_sec  + (double)start.tv_usec / 1e6)); 
  printf ("Time taken: %f (secs)\n", time_taken);

  printf ("Closing New Socket \n");
  close(newSocket);

  printf ("Closing Welcome Socket \n");
  close(welcomeSocket);

  printf ("Finished server ...\n");
  fflush(stdout);
}



int main(int argc, char** argv) {
    
    srand(1);

    if (argc < 4) {
        printf ("Not enough args: ./tgen [client or server] server_ip server_port type [rate or periodic or poisson] params\n");
        exit(0);
    }

    char * server_ip = argv[2];
    int server_port = atoi(argv[3]);
    char * cmd = argv[1];

    if (strcmp(cmd, "client") == 0) {
        if (argc < 6) {
            printf ("Not enough args for client: ./tgen [client or server] server_ip server_port type [rate or periodic or poisson] param1 param2 ...\n");
            exit(0);
        }
    }

    if (strcmp(argv[1], "client") == 0) {
        int param = atoi(argv[5]);
        int burst_size_kb = DEFAULT_BURST_SIZE_KB;
        if (argc == 7)
            burst_size_kb = atoi(argv[6]);
        if (strcmp(argv[4], "rate") == 0) {
            tcp_client_rate_limited(server_ip, server_port, param);
        } else if (strcmp(argv[4], "periodic") == 0) {
            tcp_client_periodic(server_ip, server_port, param, burst_size_kb);
        } else if (strcmp(argv[4], "poisson") == 0) {
            tcp_client_poisson(server_ip, server_port, param, burst_size_kb);
        } else {
            printf ("Unsupported tgen type: %s\n", argv[4]);
            exit(0);
        }
        
    } else {
        tcp_server(server_ip, server_port);
    }
    return 0;

}
