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
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#define NRA 2000                 /* number of rows in matrix A */
#define NCA 2000                 /* number of columns in matrix A */
#define NCB 2000                  /* number of columns in matrix B */

double a[NRA][NCA];
double b[NCA][NCB];           /* matrix B to be multiplied */
double c[NRA][NCB];  	      /* result matrix C */


double curr_time() {
    struct timeval tv;
    unsigned long timeInMicroseconds;
    double time;
    gettimeofday(&tv,NULL);
    timeInMicroseconds = tv.tv_sec*(unsigned long)1000000+tv.tv_usec;
    time = (double)timeInMicroseconds/(double)1000000;
    return time;
}

int main (int argc, char *argv[]) {
   int  i, j, k, rc;           	 /* misc */
   
   double startTime = curr_time();
   double elapsedTime;
      rc = -1;
      printf ("Initializing !\n");
      fflush(stdout);

      for (i=0; i<NRA; i++)
         for (j=0; j<NCA; j++)
            a[i][j]= i+j;

      for (i=0; i<NCA; i++)
         for (j=0; j<NCB; j++)
            b[i][j]= i*j;

      printf ("Initialized !\n");
      fflush(stdout);

      for (k=0; k<NCB; k++) {
            for (i=0; i<NRA; i++) {
               c[i][k] = 0.0;
               for (j=0; j<NCA; j++)
                  c[i][k] = c[i][k] + a[i][j] * b[j][k];
            }
      }

      printf ("Multiplied !\n");
      fflush(stdout);

      for (i=0; i<NRA; i++) {
	for (k=0; k<NCB; k++) {
		if (c[i][k] > rc) {
			rc = c[i][k];
		}

	}
      }

      printf ("RC = %d\n", rc);
      elapsedTime = curr_time() - startTime;
      printf ("Time taken: %f (secs)\n", elapsedTime);
      fflush(stdout);

      return 0;
}
