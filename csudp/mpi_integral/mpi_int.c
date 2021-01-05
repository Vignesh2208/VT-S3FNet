# include <math.h>
# include <vtmpi.h>
# include <stdio.h>
# include <stdlib.h>
# include <time.h>

double f (double x);
void timestamp ();

/******************************************************************************/

int main ( int argc, char *argv[] ) {
  double a;
  double b;
  double error;
  double exact;
  int i;
  int master = 0;
  double my_a;
  double my_b;
  int my_id;
  int my_n;
  double my_total;
  int n;
  int p;
  int p_num;
  int source;
  MPI_Status status;
  int tag;
  int target;
  double total;
  double wtime;
  double x;
  int integ_no = 0;

  a =  0.0;
  b = 10.0;
  n = 100000000;
  exact = 0.49936338107645674464;

  double avgJobCompletionTime = 0;
  double avgJobCommunicationTime = 0;
  double avgJobComputationTime = 0;

  double startTime;
  double elapsedTime;

  MPI_Init ( &argc, &argv );
  MPI_Comm_rank ( MPI_COMM_WORLD, &my_id );
  MPI_Comm_size ( MPI_COMM_WORLD, &p_num );

  /*
  We want N to be the total number of evaluations.
  If necessary, we adjust N to be divisible by the number of processes.
  */
  my_n = n / ( p_num - 1 );
  n = ( p_num - 1 ) * my_n;
  my_n = 100000000;

  if ( my_id == master ) {
    wtime = MPI_Wtime ( );
    timestamp ( );
    printf ( "\n" );
    printf ( "QUAD_MPI\n" );
    printf ( "  C/MPI version\n" );
    printf ( "  Estimate an integral of f(x) from A to B.\n" );
    printf ( "  f(x) = 50 / (pi * ( 2500 * x * x + 1 ) )\n" );
    printf ( "\n" );
    printf ( "  A = %f\n", a );
    printf ( "  B = %f\n", b );
    printf ( "  N = %d\n", n );
    printf ( "  EXACT = %24.16f\n", exact );
    printf ( "\n" );
    printf ( "  Use MPI to divide the computation among\n" );
    printf ( "  multiple processes.\n" );
  }

  source = master;
  /*
  Process 0 assigns each process a subinterval of [A,B].
  */
  if ( my_id == master ) {

    while (1) {
        total = 0.0;
        my_total = 0.0;
        a += 10.0;
        b += 10.0;

        startTime = MPI_Wtime();

        printf ("Sending partitions over to workers !\n");
        fflush(stdout);
        for ( p = 1; p <= p_num - 1; p++ ) {
            my_a = ( ( double ) ( p_num - p     ) * a   
                    + ( double ) (         p - 1 ) * b ) 
                    / ( double ) ( p_num     - 1 );

            target = p;
            tag = 1;
            MPI_Send ( &my_a, 1, MPI_DOUBLE, target, tag, MPI_COMM_WORLD );

            my_b = ( ( double ) ( p_num - p - 1 ) * a   
                    + ( double ) (         p     ) * b ) 
                    / ( double ) ( p_num     - 1 );

            target = p;
            tag = 2;
            MPI_Send ( &my_b, 1, MPI_DOUBLE, target, tag, MPI_COMM_WORLD );
        }

        printf ("Waiting to receive integral partitions from workers !\n");
        fflush(stdout);
        for ( p = 1; p <= p_num - 1; p++ ) {
            source = p;
            tag = 1;
            MPI_Recv ( &my_total, 1, MPI_DOUBLE, source, tag, MPI_COMM_WORLD, &status );
            total += my_total;
        }

        printf ("Computed integral: %d over interval [%f, %f] = %f\n", integ_no,
            a, b, total);

        elapsedTime = MPI_Wtime() - startTime;
        avgJobCompletionTime += elapsedTime;

        printf ("Avg-Job-Completion-Time = %f (sec)\n", avgJobCompletionTime/(integ_no + 1));
        fflush(stdout);

        printf ("\n------------------------------------------------------------------------------\n");
        fflush(stdout);
        integ_no ++;

    }
    

  } else {

    while (1) {
        
        startTime = MPI_Wtime();
        printf ("Waiting to receive partition information from master !\n");
        fflush(stdout);

        source = master;
        tag = 1;
        MPI_Recv ( &my_a, 1, MPI_DOUBLE, source, tag, MPI_COMM_WORLD, &status );

        source = master;
        tag = 2;
        MPI_Recv ( &my_b, 1, MPI_DOUBLE, source, tag, MPI_COMM_WORLD, &status );

        printf ("Process %d computing itegral over my_a = %f, my_b= %f\n", my_id, my_a, my_b);
        fflush(stdout);

        elapsedTime = MPI_Wtime() - startTime;
        avgJobCommunicationTime += elapsedTime;

        startTime = MPI_Wtime();
        my_total = 0.0;
        for ( i = 1; i <= my_n; i++ ) {
            x = ((double)(my_n - i) * my_a  + (double ) (i - 1) * my_b ) / (double) (my_n - 1);
            my_total = my_total + f(x);
        }

        my_total = (my_b - my_a) * my_total / ( double ) (my_n);

        elapsedTime = MPI_Wtime() - startTime;
        avgJobComputationTime += elapsedTime;
         
        startTime = MPI_Wtime();
        target = master;
        tag = 1;
        MPI_Send ( &my_total, 1, MPI_DOUBLE, target, tag, MPI_COMM_WORLD );
        elapsedTime = MPI_Wtime() - startTime;
        avgJobCommunicationTime += elapsedTime;


        if (avgJobCommunicationTime) {
          printf ("Avg-Compute-Communication-Ratio = %f\n", 
              avgJobComputationTime/avgJobCommunicationTime);
          fflush(stdout);
        }


        printf ("Process %d contributed MY_TOTAL = %f, my_a = %f, my_b= %f\n", my_id, my_total , my_a, my_b);
        printf ("Integral: %d computed\n", integ_no);
        printf ("\n------------------------------------------------------------------------------\n");
        fflush(stdout);

        integ_no ++;
    }
  }
  MPI_Finalize ();
  return 0;
}
/******************************************************************************/

/******************************************************************************/
/*
  Purpose:
    F evaluates the function.
*/
double f ( double x ) {
  double pi;
  double value;

  pi = 3.141592653589793;
  //value = 50.0 / ( pi * ( 2500.0 * x * x + 1.0 ) );
  value = (pi * ( 2500.0 * x * x + 1.0 ) );
  

  return value;
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
