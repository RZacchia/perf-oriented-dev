#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


typedef unsigned long dn;

dn delannoy(dn x, dn y) {
	dn *row = malloc(sizeof(dn) * (x + 1));
	if(row == NULL) {
		fprintf(stderr, "Memory allocation failed\n");
		exit(EXIT_FAILURE);
	}

	for (dn i = 0; i <= x; ++i) {
		row[i] = 1;
	}
    for (dn i = 0; i < x; i++) {
        dn prev = 1;
        for (dn j = 1; j <= y; j++) {
            dn temp = row[j];
            row[j] = prev + temp + row[j - 1];
            prev = temp;
        }
    }

    // return answer
    dn result = row[y];
    free(row);
    return result;
}


dn DELANNOY_RESULTS[] = {
	1, 3, 13, 63, 321, 1683, 8989, 48639, 265729, 1462563, 8097453, 45046719, 251595969, 1409933619, 
	7923848253, 44642381823, 252055236609, 1425834724419, 8079317057869, 45849429914943, 260543813797441, 
	1482376214227923, 8443414161166173};

int NUM_RESULTS = sizeof(DELANNOY_RESULTS) / sizeof(dn);

int main(int argc, char **argv) {
	if(argc<2) {
		printf("Usage: delannoy N [+t]\n");
		exit(EXIT_FAILURE);
	}

	int n = atoi(argv[1]);
	if(n >= NUM_RESULTS) {
		printf("N too large (can only check up to %d)\n", NUM_RESULTS);
	}

	dn result = 0;
	struct timespec t0, t1;
	clock_gettime(CLOCK_MONOTONIC, &t0);
	result = delannoy(n, n);
	clock_gettime(CLOCK_MONOTONIC, &t1);	
	printf("Tabulated delannoy(%d, %d) = %lu\n", n, n, result);
	if(result == DELANNOY_RESULTS[n]) {
		printf("Verification: OK\n");
	} else {
		printf("Verification: ERR\n");
	}
	printf("result %lu\n", result);	
	unsigned long long elapsed_ns =
		(unsigned long long)(t1.tv_sec - t0.tv_sec) * 1000000000ull +
		(unsigned long long)(t1.tv_nsec - t0.tv_nsec);
	printf("time: %.3f us\n",
		(double)elapsed_ns / 1e3);
	return EXIT_SUCCESS;
}
