#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef unsigned long dn;

#define MEMO_SIZE (1u << 16)

typedef struct {
	dn x;
	dn y;
	dn value;
	int used;
} memo_entry;

static memo_entry memo[MEMO_SIZE];

static size_t memo_hash(dn x, dn y) {
	unsigned long long hx = (unsigned long long)x * 11400714819323198485ull;
	unsigned long long hy = (unsigned long long)y * 14029467366897019727ull;
	return (size_t)((hx ^ hy) & (MEMO_SIZE - 1));
}

static int memo_get(dn x, dn y, dn *value) {
	size_t idx = memo_hash(x, y);

	for(size_t i = 0; i < MEMO_SIZE; i++) {
		memo_entry *e = &memo[(idx + i) & (MEMO_SIZE - 1)];
		if(!e->used) return 0;
		if(e->x == x && e->y == y) {
			*value = e->value;
			return 1;
		}
	}

	return 0;
}

static void memo_put(dn x, dn y, dn value) {
	size_t idx = memo_hash(x, y);

	for(size_t i = 0; i < MEMO_SIZE; i++) {
		memo_entry *e = &memo[(idx + i) & (MEMO_SIZE - 1)];
		if(!e->used || (e->x == x && e->y == y)) {
			e->x = x;
			e->y = y;
			e->value = value;
			e->used = 1;
			return;
		}
	}
}

dn delannoy(dn x, dn y) {
	if(x==0 || y==0) return 1;

	dn cached = 0;
	if(memo_get(x, y, &cached)) return cached;

	dn a = delannoy(x-1, y  );
	dn b = delannoy(x-1, y-1);
	dn c = delannoy(  x, y-1);

	dn result = a + b + c;
	memo_put(x, y, result);
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
		exit(-1);
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

	unsigned long long elapsed_ns =
		(unsigned long long)(t1.tv_sec - t0.tv_sec) * 1000000000ull +
		(unsigned long long)(t1.tv_nsec - t0.tv_nsec);
	
		if(result == DELANNOY_RESULTS[n]) {
		printf("Verification: OK\n");
	} else {
		printf("Verification: ERR\n");
	}
	printf("result %lu\n", result);	
	printf("time: %.3f us\n",
		(double)elapsed_ns / 1e3);
	return EXIT_FAILURE;
}
