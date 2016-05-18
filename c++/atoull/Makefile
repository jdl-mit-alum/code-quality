#!/usr/bin/env make

MODULE=atoull
COPTS=-std=c++11 -Wall -DLETTVIN_LEXERS_H_CPP_UNIT 

all:	coverage $(MODULE).diff.txt lint doxygen
	@echo "[PASS] Compile/Execute/Compare"
	@echo "[TODO] use prof or gprof"
	@echo "[TODO] use valgrind"

.PHONY:
clean:
	@echo "Clean"
	@rm -f $(MODULE).diff.txt $(MODULE).this.txt $(MODULE).pass.txt
	@rm -f $(MODULE) $(MODULE).coverage $(MODULE).doxygen.txt
	@rm -f *.gcov *.gcda *.gcno *.lint

.PHONY:
doxygen: Doxyfile $(MODULE).h.cpp
	@echo "Doxygen"
	@doxygen > $(MODULE).doxygen.txt 2>&1
	@echo "[TODO] Fix the doxygen warnings"

.PHONY:
coverage: $(MODULE).h.cpp
	@echo "Coverage"
	@g++ --coverage $(COPTS) -o $(MODULE).coverage $<
	@./$(MODULE).coverage > /dev/null
	@gcov $< > $<.gcov

.PHONY:
lint: $(MODULE).h.cpp
	@cpplint $< > $(MODULE).lint 2>&1
	@echo "[PASS] Lint"

$(MODULE).diff.txt: $(MODULE).this.txt $(MODULE).pass.txt
	@echo "Compare $^"
	@diff -I atoull $^ > $@

$(MODULE).this.txt:	$(MODULE)
	@echo "Execute $@"
	@./$< > $@

$(MODULE):	$(MODULE).h.cpp
	@echo "Compile $@"
	@g++ $(COPTS) -o $(MODULE) $(MODULE).h.cpp
