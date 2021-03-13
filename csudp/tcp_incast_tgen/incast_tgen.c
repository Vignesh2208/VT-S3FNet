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
#include <assert.h>
#include <time.h>
#include <pthread.h>

#define US_IN_MS 1000
#define SND_BUF_SIZE 16384
#define RCV_BUF_SIZE 212992
#define MSG_SIZE 1460
#define DEFAULT_BURST_SIZE_KB 8
#define RATE_LIMIT_PERIOD_MS 10

struct server_params {
  char * server_ip;
  int server_port;
};


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


void * tcp_server(void * arg) {


  char * server_ip;
  int server_port;
  int welcomeSocket, newSocket;
  char buffer[MSG_SIZE + 10];
  struct sockaddr_in serverAddr;
  struct sockaddr_storage serverStorage;
  //int ret;
  int sndBufSize = SND_BUF_SIZE;
  int rcvBufSize = RCV_BUF_SIZE;
  //char * finishMsg = "DONE";

  assert(arg != NULL);
  struct server_params  * param = (struct server_params *)arg;
  server_ip = param->server_ip;
  server_port = param->server_port;

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

  printf ("Binding to server port: %d\n", server_port);
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
      fflush(stdout);
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

  return NULL;
}



int main(int argc, char** argv) {
    
    

    if (argc < 6) {
        printf ("Not enough args: ./tgen [client or server] seed server_ip server_port params\n");
        fflush(stdout);
        exit(0);
    }

    int seed = atoi(argv[2]);
    char * server_ip = argv[3];
    int server_port = atoi(argv[4]);
    int num_threads;
    char * cmd = argv[1];
    pthread_t *thread_ids;
    struct server_params * thread_args;
    int i;

    if (strcmp(cmd, "client") == 0) {
        if (argc < 6) {
            printf ("Not enough args for client: ./tgen [client or server] seed server_ip server_port param1 param2 ...\n");
            fflush(stdout);
            exit(0);
        }
    } else {
      num_threads = atoi(argv[5]);
      assert(num_threads > 0);
    }

    srand(seed);

    if (strcmp(argv[1], "client") == 0) {
        int param = atoi(argv[5]);
        int burst_size_kb = DEFAULT_BURST_SIZE_KB;
        if (argc == 7)
            burst_size_kb = atoi(argv[6]);
        
        tcp_client_poisson(server_ip, server_port, param, burst_size_kb);
    } else {
        thread_ids = (pthread_t * )malloc (sizeof(pthread_t) * num_threads);
        thread_args = (struct server_params *)malloc(sizeof (struct server_params) * num_threads);

        for (i = 0; i < num_threads; i++) {
          thread_args[i].server_ip = server_ip;
          thread_args[i].server_port = server_port + i;
          pthread_create(&thread_ids[i], NULL, tcp_server, &thread_args[i]);
        }
        for (i = 0; i < num_threads; i++) {
          pthread_join( thread_ids[i], NULL);
        }
        
    }
    return 0;

}
