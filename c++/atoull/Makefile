#!/usr/bin/env make

STARTS="starts Basic style"
ENDS="ends Basic style"

all:	coverage atoull.diff.txt lint doxygen
	@echo "[PASS] Compile/Execute/Compare"

.PHONY:
clean:
	@echo "Clean"
	@rm -f atoull.diff.txt atoull.this.txt atoull atoull.coverage
	@rm -f *.gcov *.gcda *.gcno *.lint

.PHONY:
doxygen: atoull.h.cpp
	@echo "Doxygen"
	@doxygen $<
	@echo "TODO Fix the doxygen warnings"

.PHONY:
coverage: atoull.h.cpp
	@echo "Coverage"
	@g++ --coverage -Wall -DLETTVIN_LEXERS_H_CPP_UNIT -o atoull.coverage $<
	@./atoull.coverage
	@gcov $< > $<.gcov

.PHONY:
lint: atoull.h.cpp
	@cpplint $< > atoull.lint 2>&1
	@echo "[PASS] Lint"

atoull.diff.txt: atoull.this.txt atoull.pass.txt
	@echo "Compare $^"
	@diff $^ > $@

atoull.this.txt:	atoull
	@echo "Execute $@"
	@./$< | grep -v $(STARTS) | grep -v $(ENDS) > $@

atoull:	atoull.h.cpp
	@echo "Compile $@"
	@g++ -Wall -DLETTVIN_LEXERS_H_CPP_UNIT -o atoull atoull.h.cpp
