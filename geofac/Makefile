# Makefile for Geometric Factorization (geofac)
# Standalone build - no cross-directory dependencies

CC = clang
CFLAGS = -std=c99 -Wall -Wextra -O3 -I../shared
LDFLAGS = -lmpfr -lgmp -lm -lssl -lcrypto

# Optional OpenMP support
ifdef WITH_OPENMP
CFLAGS += -DWITH_OPENMP -fopenmp
LDFLAGS += -fopenmp
endif

# macOS Homebrew paths (adjust for your system)
ifdef HOMEBREW
CFLAGS += -I/opt/homebrew/include
LDFLAGS += -L/opt/homebrew/lib
endif

TARGET = bin/geofac
SRC = src/main.c src/geofac.c src/golden_spiral.c
OBJ = $(SRC:src/%.c=build/%.o)

.PHONY: all clean dirs test

all: dirs $(TARGET)

dirs:
	mkdir -p bin build

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

build/%.o: src/%.c
	$(CC) $(CFLAGS) -c $< -o $@

test: $(TARGET)
	./tests/smoke_test.sh

clean:
	rm -f $(TARGET) $(OBJ)
	rm -rf bin build
