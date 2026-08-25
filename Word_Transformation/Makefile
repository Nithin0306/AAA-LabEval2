CXX      = g++
CXXFLAGS = -std=c++17 -O2
TARGET   = 429_1
TESTS    = 1 2 3

.PHONY: all run clean

all: $(TARGET)

$(TARGET): 429_1.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) 429_1.cpp

run: $(TARGET)
	@pass=0; fail=0; \
	for t in $(TESTS); do \
		actual=$$(./$(TARGET) < test_case_$$t.txt); \
		expected=$$(cat expected_output_$$t.txt); \
		if [ "$$actual" = "$$expected" ]; then \
			echo "Test $$t: PASS"; \
			pass=$$((pass + 1)); \
		else \
			echo "Test $$t: FAIL"; \
			echo "  expected : $$expected"; \
			echo "  got      : $$actual"; \
			fail=$$((fail + 1)); \
		fi; \
	done; \
	echo ""; \
	echo "Results: $$pass passed, $$fail failed"

clean:
	rm -f $(TARGET)
