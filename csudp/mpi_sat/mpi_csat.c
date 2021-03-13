# include <stdlib.h>
# include <stdio.h>
# include <vtmpi.h>
# include <time.h>

#define MASTER 0               /* taskid of first task */
#define FROM_MASTER 1          /* setting a message type */
#define FROM_WORKER 2          /* setting a message type */


int main ( int argc, char *argv[] );
int circuit_value ( int n, int bvec[] );
void print_bvec(int n, int bvec[] );
void timestamp ();

/******************************************************************************/

int main ( int argc, char *argv[] ) {
  # define N 30
  int bvec[N];
  int i;
  int id;
  int ihi;
  int ihi2;
  int ilo;
  int ilo2;
  int j;
  int k;
  int n = N;
  int p;
  int solution_num_local;
  int solution_num;
  int value;
  int status;
  double wtime;
  double avgJobCompletionTime = 0;
  double avgJobCommunicationTime = 0;
  double avgJobComputationTime = 0;
  double startTime;
  double elapsedTime;
  int trigger;
  int task_no = 1;
  int per_task_iters;
  int i4;

  MPI_Init ( &argc, &argv );
  MPI_Comm_rank ( MPI_COMM_WORLD, &id );
  MPI_Comm_size ( MPI_COMM_WORLD, &p );
  /*
  Let process 0 print the opening remarks.
  */
  if ( id == 0 ) {
    timestamp ( );
    printf ( "\n" );
    printf ( "SATISFY_MPI\n" );
    printf ( "  C/MPI version\n" );
    printf ( "  We have a logical function of N logical arguments.\n" );
    printf ( "  We do an exhaustive search of all 2^N possibilities,\n" );
    printf ( "  seeking those inputs that make the function TRUE.\n" );
    fflush(stdout);
}
  /*
  The BIG calculation goes from 0 = ILO <= I < IHI = 2*N.
  Compute the upper limit.
  */
  ilo = 0;

  ihi = 1;
  for ( i = 1; i <= n; i++ ) {
    ihi = ihi * 2;
  }

  per_task_iters = ihi / p;

  if ( id == 0 ) {
    printf ( "\n" );
    printf ( "  The number of logical variables is N = %d\n", n );
    printf ( "  The number of input vectors to check is %d\n", ihi );
    printf ( "\n" );
    printf ( "# Worker       Index    ---------Input Values------------------------\n" );
    printf ( "\n" );
    fflush(stdout);
  }
  /*
  Processor ID takes the interval ILO2 <= I < IHI2.
  Using the formulas below yields a set of nonintersecting intervals
  which cover the original interval [ILO,IHI).
  */

  while (1) {

    printf ( "\n-------------------------------------------------------------\n" );
    printf ( "  Task no: %d\n", task_no);
    fflush(stdout);

    if ( id == 0 ) {
        wtime = MPI_Wtime();
    }

    // Normally each iteration should change something e.g the function itself.
    // In this example we are not changing the function. We are just artificially introducing a
    // synchronization barrier

    if (id == 0) {
        // Broadcast trigger
        MPI_Bcast(&trigger, 1, MPI_INT, MASTER, MPI_COMM_WORLD);
        
    } else {
        printf ("Waiting for trigger !\n");
        fflush(stdout);
        startTime = MPI_Wtime();
        // Wait for trigger
        MPI_Bcast(&trigger, 1, MPI_INT, MASTER, MPI_COMM_WORLD);
        elapsedTime = MPI_Wtime() - startTime;
        avgJobCommunicationTime += elapsedTime;
    }

    startTime = MPI_Wtime();

    if (id == 0) {
      ilo2 = ilo;
      ihi2 = ilo2 + per_task_iters - 1;
    } else if (id == p - 1) {
      ilo2 = ilo + id * per_task_iters;
      ihi2 = ihi;
    } else {
      ilo2 = ilo + id * per_task_iters;
      ihi2 = ilo2 + per_task_iters - 1;
    }
    printf ( "  Worker %d iterates from %d <= I < %d\n", id, ilo2, ihi2 );
    printf ( "\n" );
    fflush(stdout);

    /*
    Check if BVEC is a solution.  Then "increment" BVEC.
    */
    solution_num_local = 0;      
    for ( i = ilo2; i < ihi2; i++ ) {
        i4 = i;
        // convert i to a vector
	for ( k = n - 1; k >= 0; k-- ) {
    	   bvec[k] = i4 % 2;
    	   i4 = i4 / 2;
  	}
        value = circuit_value (n,bvec);
        if ( value == 1 ) {
            solution_num_local = solution_num_local + 1;
            printf ( "  %2d  %8d  %10d:  ", solution_num_local, id, i );
            print_bvec(n, bvec);
            printf ( "\n" );
            fflush(stdout);
        }
    }
    elapsedTime = MPI_Wtime() - startTime;
    avgJobComputationTime += elapsedTime;

    /*
    Process 0 gathers the local solution totals.
    */
    if (id == 0) {
        printf ("Master-node waiting for results from other workers !\n");
        fflush(stdout);
        for (i = 1; i < p; i++) {
            MPI_Recv(&solution_num, 1, MPI_INT, i, FROM_WORKER, MPI_COMM_WORLD, &status);
            solution_num_local += solution_num;
        }
    } else {
        printf ("Sending results to master node !\n");
        fflush(stdout);
        startTime = MPI_Wtime();
        MPI_Send(&solution_num_local, 1, MPI_INT, MASTER, FROM_WORKER, MPI_COMM_WORLD);
        elapsedTime = MPI_Wtime() - startTime;
        avgJobCommunicationTime += elapsedTime;
    }
    /*
    Let process 0 print the closing remarks.
    */
    if ( id == 0 ) {
        wtime = MPI_Wtime() - wtime;
        avgJobCompletionTime += wtime;
        printf ( "\n" );
        printf ( "Number of solutions found was: %d\n", solution_num_local);
        printf ( "Avg-Job-Completion-Time = %f (sec)\n", avgJobCompletionTime / (task_no));
        fflush(stdout);
    } else {
        if (avgJobCommunicationTime) {
            printf ("Avg-Compute-Communication-Ratio = %f\n", 
               avgJobComputationTime/avgJobCommunicationTime);
            fflush(stdout);
        }
    }

    task_no ++;
  }

  /*
  Terminate MPI.
  */
  MPI_Finalize ( );

  /*
  Terminate.
  */
  if ( id == 0 ) {
    printf ( "\n" );
    printf ( "SATISFY_MPI\n" );
    printf ( "  Normal end of execution.\n" );
    printf ( "\n" );
    timestamp ( );
  }
  return 0;
  # undef N
}
/******************************************************************************/

int circuit_value ( int n, int bvec[] ) {
  int value;

  value = 
       (  bvec[0]  ||  bvec[1]  )
    && ( !bvec[1]  || !bvec[3]  )
    && (  bvec[2]  ||  bvec[3]  )
    && ( !bvec[3]  || !bvec[4]  )
    && (  bvec[4]  || !bvec[5]  )
    && (  bvec[5]  || !bvec[6]  )
    && (  bvec[5]  ||  bvec[6]  )
    && (  bvec[6]  || !bvec[15] )
    && (  bvec[7]  || !bvec[8]  )
    && ( !bvec[7]  || !bvec[13] )
    && (  bvec[8]  ||  bvec[9]  )
    && (  bvec[8]  || !bvec[9]  )
    && ( !bvec[9]  || !bvec[10] )
    && (  bvec[9]  ||  bvec[11] )
    && (  bvec[10] ||  bvec[11] )
    && (  bvec[12] ||  bvec[13] )
    && (  bvec[13] || !bvec[14] )
    && (  bvec[14] ||  bvec[15] )
    && (  bvec[14] ||  bvec[16] )
    && (  bvec[17] ||  bvec[1]  )
    && (  bvec[18] || !bvec[0]  )
    && (  bvec[19] ||  bvec[1]  )
    && (  bvec[19] || !bvec[18] )
    && ( !bvec[19] || !bvec[9]  )
    && (  bvec[0]  ||  bvec[17] )
    && ( !bvec[1]  ||  bvec[20] )
    && ( !bvec[21] ||  bvec[20] )
    && ( !bvec[22] ||  bvec[20] )
    && ( !bvec[21] || !bvec[20] )
    && (  bvec[22] || !bvec[20] )
    && (  bvec[23]  ||  bvec[24])
    && ( !bvec[24]  || !bvec[26])
    && (  bvec[25]  ||  bvec[26])
    && ( !bvec[26]  || !bvec[27]);

  return value;
}
/******************************************************************************/

void print_bvec(int n, int bvec[] ) {
  int i;
  for ( i = 0; i < n; i++ ) {
      printf ( " %d", bvec[i] );
  }
}
/******************************************************************************/

void timestamp ( void ) {
  # define TIME_SIZE 40

  static char time_buffer[TIME_SIZE];
  const struct tm *tm;
  time_t now;
  now = time ( NULL );
  tm = localtime ( &now );
  strftime ( time_buffer, TIME_SIZE, "%d %B %Y %I:%M:%S %p", tm );
  printf ( "%s\n", time_buffer );

  return;
  # undef TIME_SIZE
}
