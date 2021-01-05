/******************************************************************************
* FILE: mpi_mm.c
* DESCRIPTION:  
*   MPI Matrix-Vector Multiply - C Version
*   In this code, the master task distributes a matrix-vector multiply
*   operation to numtasks-1 worker tasks.
******************************************************************************/
#include <vtmpi.h>
#include <stdio.h>
#include <stdlib.h>

#define NR 2000
#define NC 2000
#define N 500                 /* square matrix size */
#define MASTER 0               /* taskid of first task */
#define FROM_MASTER 1          /* setting a message type */
#define FROM_WORKER 2          /* setting a message type */


double   x[NC];
double   v[NR];
double   r[NR];
double	a[NR][NC];             /* matrix A to be multiplied */
double   b[NC][NR];             /* matrix B to be multiplied */
double   c[NR][NR];             /* result matrix C */

int main (int argc, char *argv[]) {
   int numtasks,          /* number of tasks in partition */
	taskid,                /* a task identifier */
	numworkers,            /* number of worker tasks */
	source,                /* task id of message source */
	dest,                  /* task id of message destination */
	mtype,                 /* message type */
	rows,                  /* rows of matrix A sent to each worker */
	averow, extra, offset, /* used to determine rows sent to each worker */
	i, j, k, rc;           /* misc */

   double avgJobCompletionTime = 0;
   double avgJobCommunicationTime = 0;
   double avgJobComputationTime = 0;

   double startTime;
   double elapsedTime;
   
   MPI_Status status;

   int msg_no = 0;

   MPI_Init(&argc,&argv);
   MPI_Comm_rank(MPI_COMM_WORLD,&taskid);
   MPI_Comm_size(MPI_COMM_WORLD,&numtasks);
   if (numtasks < 2 ) {
      printf("Need at least two MPI tasks. Quitting...\n");
      exit(1);
   }
   numworkers = numtasks-1;


    /**************************** master task ************************************/
   if (taskid == MASTER) {

      

      // Partition and send matrix A once to workers
      averow = NR / numworkers;
      extra = NR % numworkers;
      offset = 0;
      mtype = FROM_MASTER;

      for (dest=1; dest<=numworkers; dest++) {
         rows = (dest <= extra) ? averow+1 : averow; 
         printf("Sending %d rows to task %d offset=%d\n",rows, dest, offset);

         printf("Sending offset = %d to dest = %d\n",offset, dest);
         MPI_Send(&offset, 1, MPI_INT, dest, mtype, MPI_COMM_WORLD);  	
         
         printf("Sending partition size (rows) = %d to dest = %d\n",rows,dest);
         MPI_Send(&rows, 1, MPI_INT, dest, mtype, MPI_COMM_WORLD);

         offset = offset + rows;
	      printf("A-matrix partition size sent to worker:  %d\n", dest);
	      fflush(stdout);
      }

      printf("\n******************************************************\n");
      printf("mpi_mm has started with %d tasks.\n", numtasks);
      while (1) {
         
         startTime = MPI_Wtime();
         printf("Initializing X vector...\n");

         for (i=0; i<NC; i++)
            x[i] = i*i;

         for (i=0; i <NR; i++)
            v[i] = i*i*i;

         // Send x-vector to the worker tasks

         // Broadcast x
         MPI_Bcast(x, NC, MPI_DOUBLE, MASTER, MPI_COMM_WORLD);

         // Broadcast v
         MPI_Bcast(v, NC, MPI_DOUBLE, MASTER, MPI_COMM_WORLD);

         printf ("Broadcasted X and V to all workers !\n");
         fflush(stdout);

         // Receive results from worker tasks
         mtype = FROM_WORKER;
         char * buf = (char *)r;
         for (i=1; i<=numworkers; i++) {
            source = i;
            
            MPI_Recv(&offset, 1, MPI_INT, source, mtype, MPI_COMM_WORLD, &status);
            printf ("Received offset = %d from %d\n", offset, source);
            fflush(stdout);

            MPI_Recv(&rows, 1, MPI_INT, source, mtype, MPI_COMM_WORLD, &status);
            printf ("Received rows = %d from %d\n", rows, source);
            fflush(stdout);


            MPI_Recv(buf, rows, MPI_DOUBLE, source, mtype, 
                     MPI_COMM_WORLD, &status);

            buf = buf + (i - 1)*rows*sizeof(double);
            printf("Received results from task %d\n",source);
            fflush(stdout);
         }

         printf ("MSG: %d Done.\n", msg_no);
         

         elapsedTime = MPI_Wtime() - startTime;
         avgJobCompletionTime += elapsedTime;

         printf ("Avg-Job-Completion-Time = %f (sec)\n", avgJobCompletionTime/(msg_no + 1));
         printf("\n******************************************************\n");
         fflush(stdout);

         msg_no ++;

      }
   }


   /**************************** worker task ************************************/
   if (taskid > MASTER) {

      mtype = FROM_MASTER;
      MPI_Recv(&offset, 1, MPI_INT, MASTER, mtype, MPI_COMM_WORLD, &status);
      MPI_Recv(&rows, 1, MPI_INT, MASTER, mtype, MPI_COMM_WORLD, &status);
      printf ("Received matrix-A partition size: %d from master !\n", rows);

      while (1) {
         printf("\n******************************************************\n");
         mtype = FROM_MASTER;
         
         startTime = MPI_Wtime();
         //MPI_Recv(x, NC, MPI_DOUBLE, MASTER, mtype, MPI_COMM_WORLD, &status);
         // Receive x
         MPI_Bcast(x, NC, MPI_DOUBLE, MASTER, MPI_COMM_WORLD);

         // Receive v
         MPI_Bcast(v, NC, MPI_DOUBLE, MASTER, MPI_COMM_WORLD);

         printf ("Received vector X and V from master \n");
         fflush(stdout);

         elapsedTime = MPI_Wtime() - startTime;
         avgJobCommunicationTime += elapsedTime;

         startTime = MPI_Wtime();

         // Just some random A(x) and B(x) matrices
         for (i = 0; i < rows; i++) {
            for (j = 0; j < NC; j++) {
               a[i][j] = x[j]*i;
            }
         }

         for (i = 0; i < NC; i++) {
            for (j = 0; j < NR; j++) {
               b[i][j] = (x[i] + 1)*j;
            }
         }

         // Multiply A(x)-partition and B(x) matrices to get C(x)-partition
         for (k=0; k< NR; k++) {
            for (i=0; i<rows; i++) {
               c[i][k] = 0.0;
               for (j=0; j< NC; j++)
                  c[i][k] = c[i][k] + a[i][j] * b[j][k];
            }
         }

         // Multiply C(x) with V
         for (i = 0; i < rows; i++) {
            for (k = 0; k < NR; k++) {
               r[i] = c[i][k] * v[k];
            }
         }
         
         elapsedTime = MPI_Wtime() - startTime;
         avgJobComputationTime += elapsedTime;


         startTime = MPI_Wtime();
         // Return r partition to master
         mtype = FROM_WORKER;
         printf ("Sending offset = %d to master !\n", offset);
         fflush(stdout);
         MPI_Send(&offset, 1, MPI_INT, MASTER, mtype, MPI_COMM_WORLD);
         printf ("Sending rows = %d to master !\n", rows);
         fflush(stdout);
         MPI_Send(&rows, 1, MPI_INT, MASTER, mtype, MPI_COMM_WORLD);
         printf ("Sending result vector partition to master!\n");
         fflush(stdout);
      
         MPI_Send(r, rows, MPI_DOUBLE, MASTER, mtype, MPI_COMM_WORLD);
         printf ("Sent results to master \n");
         fflush(stdout);

         elapsedTime = MPI_Wtime() - startTime;
         avgJobCommunicationTime += elapsedTime;

         printf ("MSG: %d Done.\n", msg_no);
         fflush(stdout);

         if (avgJobCommunicationTime) {
            printf ("Avg-Compute-Communication-Ratio = %f\n", 
               avgJobComputationTime/avgJobCommunicationTime);
            fflush(stdout);
         }

         msg_no ++;

      }
   }
  
   MPI_Finalize();
   return 0;
}
