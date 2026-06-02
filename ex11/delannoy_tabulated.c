#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long dn;

dn delannoy(dn x, dn y) {
	if(x==0 || y==0) return 1;
	dn **table = malloc(sizeof(dn *) * x);
	if(table == NULL) {
		fprintf(stderr, "Memory allocation failed\n");
		exit(EXIT_FAILURE);
	}

	for (size_t i = 0; i < x; ++i){
		table[i] = malloc(sizeof(dn) * y);
		if(table[i] == NULL) {
			fprintf(stderr, "Memory allocation failed\n");
			exit(EXIT_FAILURE);
		}
	}

	for (size_t i = 0; i < x; ++i) {
		for (size_t j = 0; j < y; ++j) {
			if(i == 0 || j == 0) {
				table[i][j] = 1;
			} else {
				table[i][j] = table[i-1][j] + table[i-1][j-1] + table[i][j-1];
			}
		}
	}

	dn result = table[x-1][y-1];

	for (size_t i = 0; i < x; ++i) {
		free(table[i]);
	}
	free(table);

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
		
	}

	int n = 20;
	if(n >= NUM_RESULTS) {
		printf("N too large (can only check up to %d)\n", NUM_RESULTS);
	}

	dn result = 0;
	result = delannoy(n, n);
	
	if(result == DELANNOY_RESULTS[n]) {
		printf("Verification: OK\n");
	} else {
		printf("Verification: ERR\nResult too large to verify\n");
	}
	printf("result %llu\n", result);	
	return EXIT_SUCCESS;
}
