/******************************************************************************
* FILE: mpi_mm.c
* DESCRIPTION:  
*   MPI Matrix Multiply - C Version
*   In this code, the master task distributes a matrix multiply
*   operation to numtasks-1 worker tasks.
*   NOTE:  C and Fortran versions of this code differ because of the way
*   arrays are stored/passed.  C arrays are row-major order but Fortran
*   arrays are column-major order.
******************************************************************************/
#include <vtmpi.h>
#include <stdio.h>
#include <stdlib.h>

#define NRA 100                 /* number of rows in matrix A */
#define NCA 100                 /* number of columns in matrix A */
#define NCB 100                  /* number of columns in matrix B */
#define MASTER 0               /* taskid of first task */
#define FROM_MASTER 1          /* setting a message type */
#define FROM_WORKER 2          /* setting a message type */

int main (int argc, char *argv[]) {
   int numtasks,              /* number of tasks in partition */
	taskid,                /* a task identifier */
	numworkers,            /* number of worker tasks */
	source,                /* task id of message source */
	dest,                  /* task id of message destination */
	mtype,                 /* message type */
	rows,                  /* rows of matrix A sent to each worker */
	averow, extra, offset, /* used to determine rows sent to each worker */
	i, j, k, rc;           /* misc */
   double	a[NRA][NCA],           /* matrix A to be multiplied */
	b[NCA][NCB],           /* matrix B to be multiplied */
	c[NRA][NCB];           /* result matrix C */
   MPI_Status status;

   int msg_no = 1;

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

      while (1) {
      printf("\n******************************************************\n");
      printf("mpi_mm has started with %d tasks.\n", numtasks);
      printf("Initializing arrays...\n");
      for (i=0; i<NRA; i++)
         for (j=0; j<NCA; j++)
            a[i][j]= i+j;
      for (i=0; i<NCA; i++)
         for (j=0; j<NCB; j++)
            b[i][j]= i*j;

      // Send matrix data to the worker tasks
      averow = NRA/numworkers;
      extra = NRA%numworkers;
      offset = 0;
      mtype = FROM_MASTER;
      for (dest=1; dest<=numworkers; dest++) {
         rows = (dest <= extra) ? averow+1 : averow;   	
         printf("Sending %d rows to task %d offset=%d\n",rows,dest,offset);

         printf("Sending offset = %d to dest = %d\n",offset,dest);
         MPI_Send(&offset, 1, MPI_INT, dest, mtype, MPI_COMM_WORLD);

         printf("Sending rows = %d to dest = %d\n",rows,dest);
         MPI_Send(&rows, 1, MPI_INT, dest, mtype, MPI_COMM_WORLD);

         printf ("Sending a rows to %d\n", dest);
         MPI_Send(&a[offset][0], rows*NCA, MPI_DOUBLE, dest, mtype,
                   MPI_COMM_WORLD);

         printf ("Sending b rows to %d\n", dest);
         MPI_Send(&b, NCA*NCB, MPI_DOUBLE, dest, mtype, MPI_COMM_WORLD);
         offset = offset + rows;
	      printf("All cmds sent \n");
	      fflush(stdout);
      }

      // Receive results from worker tasks
      mtype = FROM_WORKER;
      for (i=1; i<=numworkers; i++) {
         source = i;
         
         MPI_Recv(&offset, 1, MPI_INT, source, mtype, MPI_COMM_WORLD, &status);
         printf ("Received offset = %d from %d\n", offset, source);
         fflush(stdout);
         MPI_Recv(&rows, 1, MPI_INT, source, mtype, MPI_COMM_WORLD, &status);
         printf ("Received rows = %d from %d\n", rows, source);
         fflush(stdout);

         MPI_Recv(&c[offset][0], rows*NCB, MPI_DOUBLE, source, mtype, 
                  MPI_COMM_WORLD, &status);
         printf("Received results from task %d\n",source);
	      fflush(stdout);
      }

      printf ("MSG: %d Done.\n", msg_no);
      fflush(stdout);

      msg_no ++;

      }
   }


   /**************************** worker task ************************************/
   if (taskid > MASTER) {

      while (1) {
      printf("\n******************************************************\n");
      mtype = FROM_MASTER;
      MPI_Recv(&offset, 1, MPI_INT, MASTER, mtype, MPI_COMM_WORLD, &status);
      MPI_Recv(&rows, 1, MPI_INT, MASTER, mtype, MPI_COMM_WORLD, &status);
      MPI_Recv(&a, rows*NCA, MPI_DOUBLE, MASTER, mtype, MPI_COMM_WORLD, &status);
      MPI_Recv(&b, NCA*NCB, MPI_DOUBLE, MASTER, mtype, MPI_COMM_WORLD, &status);
      printf ("Rx cmds from master \n");
      fflush(stdout);

      for (k=0; k<NCB; k++) {
         for (i=0; i<rows; i++) {
            c[i][k] = 0.0;
         }
      }

      //for (int p = 0; p < 1000; p++) {
         for (k=0; k<NCB; k++) {
            for (i=0; i<rows; i++) {
               for (j=0; j<NCA; j++)
                  c[i][k] = c[i][k] + a[i][j] * b[j][k];
            }
         }
      //}

      mtype = FROM_WORKER;
      printf ("Sending offset = %d to master !\n", offset);
      fflush(stdout);
      MPI_Send(&offset, 1, MPI_INT, MASTER, mtype, MPI_COMM_WORLD);
      printf ("Sending rows = %d to master !\n", rows);
      fflush(stdout);
      MPI_Send(&rows, 1, MPI_INT, MASTER, mtype, MPI_COMM_WORLD);
      printf ("Sending all rows to master!\n");
      fflush(stdout);
      MPI_Send(&c, rows*NCB, MPI_DOUBLE, MASTER, mtype, MPI_COMM_WORLD);
      printf ("Sent results to master \n");
      fflush(stdout);

      printf ("MSG: %d Done.\n", msg_no);
      fflush(stdout);

      msg_no ++;

      }
   }
  
   MPI_Finalize();
   //while(1);
   return 0;
}