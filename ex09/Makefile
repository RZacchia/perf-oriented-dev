CXX = g++
CXXFLAGS = -std=c++23 -O2 -Wall -Wextra -Wpedantic
TARGET = container_benchmark
SOURCES = container_benchmark.cpp container.cpp
HEADERS = container.hpp node.hpp
BUILD_DIR = build

all: $(TARGET)

$(TARGET): $(SOURCES) $(HEADERS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCES)

clean:
	rm -f $(TARGET)
	rm -rf $(BUILD_DIR)

.PHONY: all clean
