# Makefile for Z5D nth-Prime Predictor
# Standalone build - requires only GMP and MPFR

CC = clang
CFLAGS = -std=c99 -Wall -Wextra -O3 -I../shared -Iinclude
LDFLAGS = -lmpfr -lgmp -lm

# macOS Homebrew paths
ifdef HOMEBREW
CFLAGS += -I/opt/homebrew/include
LDFLAGS += -L/opt/homebrew/lib
endif

TARGET = bin/z5dp
BENCH = bin/z5dp_bench
SRC_CLI = src/z5d_cli.c src/z5d_predictor.c src/z5d_math.c
SRC_BENCH = src/z5d_bench.c src/z5d_predictor.c src/z5d_math.c

.PHONY: all clean dirs test bench

all: dirs $(TARGET)

dirs:
	mkdir -p bin

$(TARGET): $(SRC_CLI)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

bench: dirs $(BENCH)

$(BENCH): $(SRC_BENCH)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^
	./$(BENCH)

test: $(TARGET)
	./tests/test_accuracy.sh

clean:
	rm -f $(TARGET) $(BENCH)
	rm -rf bin
