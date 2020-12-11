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

#define MAX_CMD_LENGTH 6
#define SND_BUF_SIZE 16384
#define RCV_BUF_SIZE 212992
#define MSG_SIZE 1460

#define NUM_BYTES_TO_SEND MSG_SIZE * 100000


void tcp_client(char * server_ip, int server_port) {

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
  printf ("Waiting for data ...\n");
  fflush(stdout);
  int numReceived = 0;

  struct timeval start, stop;
  gettimeofday(&start, NULL);
  while (numReceived < NUM_BYTES_TO_SEND) {
    int ret = recv(clientSocket, buffer, 1500, 0);
    if (ret < 0)
      break;
    numReceived += ret;
    //printf ("Rx msg size: %d\n", ret);
    fflush(stdout);
  }

  gettimeofday(&stop, NULL);
  double time_taken = ((double)stop.tv_sec + (double)stop.tv_usec / 1e6 - ((double)start.tv_sec  + (double)start.tv_usec / 1e6)); 
  
  printf ("Received msg: %s\n", buffer);
  printf ("Time taken: %f (secs)\n", time_taken);
  printf ("Rcv Throughput (Mbps) : %f\n", (NUM_BYTES_TO_SEND * 8)/(1e6 *time_taken));

  
  printf ("Closing client socket !\n");
  fflush(stdout);
  close(clientSocket);   
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
  gettimeofday(&start, NULL);

  while (numSent < NUM_BYTES_TO_SEND) {
    send(newSocket,buffer,msgLength, 0);
    numSent += msgLength;
    numChkPt += msgLength;
    if (numChkPt >= 1000000 || numSent >= NUM_BYTES_TO_SEND) {
      printf ("Sent: %d bytes\n", numSent);
      numChkPt = 0;
    }
  }
  
  gettimeofday(&stop, NULL);
  double time_taken = ((double)stop.tv_sec + (double)stop.tv_usec / 1e6 - ((double)start.tv_sec  + (double)start.tv_usec / 1e6)); 
  printf ("Time taken: %f (secs)\n", time_taken);
  printf ("Send Throughput (Mbps) : %f\n", (NUM_BYTES_TO_SEND * 8)/(1e6*time_taken));

  printf ("Closing New Socket \n");
  close(newSocket);

  printf ("Closing Welcome Socket \n");
  close(welcomeSocket);

  printf ("Finished server ...\n");
}



int main(int argc, char** argv) {
    
    
    if (argc < 4) {
        printf ("Not enough args: ./stack [client or server] server_ip server_port\n");
        exit(0);
    }

    if (strcmp(argv[1], "client") == 0) {
        tcp_client(argv[2], atoi(argv[3]));
    } else {
        tcp_server(argv[2], atoi(argv[3]));
    }
    return 0;

}
