# Makefile for SHA-256 Geometric Bounds
# Lightweight - no GMP/MPFR needed

CC = clang
CFLAGS = -std=c99 -Wall -Wextra -O3 -I../shared -Idata
LDFLAGS = -lm

TARGET = bin/sha256_bounds
SRC = src/main.c src/sha256_bounds.c src/random_baseline.c

.PHONY: all clean dirs test

all: dirs $(TARGET)

dirs:
	mkdir -p bin

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

test: $(TARGET)
	./$(TARGET) --test

clean:
	rm -f $(TARGET)
	rm -rf bin
