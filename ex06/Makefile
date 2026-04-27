CC = gcc
CFLAGS = -Wall -Wextra -g

TARGETS = cache mmul
all: $(TARGETS)

cache: cache.c
	$(CC) $(CFLAGS) -o cache cache.c

mmul: mmul.c
	$(CC) $(CFLAGS) -o mmul mmul.c

clean:
	rm -f $(TARGETS)