#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define __USE_TIME_BITS64 1

// https://eng.libretexts.org/Bookshelves/Computer_Science/Operating_Systems/Think_OS_-_A_Brief_Introduction_to_Operating_Systems_(Downey)/07%3A_Caching/7.04%3A_Measuring_cache_performance
double get_seconds(){
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC_RAW, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}
int main(int argc, char *argv[]) {
    double sec = 0.0, sec0;
    int iters = 1000 ;
    int limit =  1000;

    
    if(argc == 2) {
        if (atoi(argv[1]) <= 0 || atoi(argv[1]) % sizeof(int) != 0) {
            printf("Invalid limit provided. Using default limit: %d bytes\n", limit);
        } else {
            limit = atoi(argv[1]) / sizeof(int); 
        }
    } else if (argc == 3)
    {
        if (atoi(argv[1]) <= 0 || atoi(argv[1]) % sizeof(int) != 0) {
            printf("Invalid limit provided. Using default limit: %d bytes\n", limit);
        } else {
            limit = atoi(argv[1]) / sizeof(int); 
        }
        iters = atoi(argv[2]);
    } else {
        printf("Usage: %s <limit_in_bytes> <iters>\n", argv[0]);
        printf("Using default limit: %d bytes and iters: %d\n", limit, iters);
        limit /= sizeof(int);
    }
    
    
    int *array = (int *)malloc(limit * sizeof(int));
    // Initialize the array to ensure it's allocated in memory
    for (int index = 0; index < limit; ++index) 
            array[index] = index;

    for (int it = 0; it < iters; it++) {
        for (int index = 0; index < limit; ++index) {
            sec0 = get_seconds();
            array[index] = array[index] + 1;
            sec = sec + (get_seconds() - sec0);
        }
    }
        

    printf("Block size: %ld bytes, Avg. Access time: %.2f nanoseconds\n", limit * sizeof(int), sec / (limit * iters));

    free(array);
    return 0;
}
