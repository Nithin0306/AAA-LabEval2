CXX      = g++
CXXFLAGS = -std=c++17 -O2
IMPLS    = 321_1 321_2 321_3
TESTS    = 1 2 3

.PHONY: all run clean

all: $(IMPLS)

321_1: 321_1.cpp
	$(CXX) $(CXXFLAGS) -o 321_1 321_1.cpp

321_2: 321_2.cpp
	$(CXX) $(CXXFLAGS) -o 321_2 321_2.cpp

321_3: 321_3.cpp
	$(CXX) $(CXXFLAGS) -o 321_3 321_3.cpp

run: $(IMPLS)
	@for impl in $(IMPLS); do \
		echo "=== $$impl ==="; \
		pass=0; fail=0; \
		for t in $(TESTS); do \
			actual=$$(./$$impl < test_case_$$t.txt); \
			expected=$$(cat expected_output_$$t.txt); \
			if [ "$$actual" = "$$expected" ]; then \
				echo "  Test $$t: PASS"; \
				pass=$$((pass + 1)); \
			else \
				echo "  Test $$t: FAIL"; \
				echo "    expected : $$expected"; \
				echo "    got      : $$actual"; \
				fail=$$((fail + 1)); \
			fi; \
		done; \
		echo "  Results: $$pass passed, $$fail failed"; \
		echo ""; \
	done

clean:
	rm -f $(IMPLS)
