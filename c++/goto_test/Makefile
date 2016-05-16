#!/usr/bin/env make

STARTS="starts Basic style"
ENDS="ends Basic style"

all:	coverage goto_test.diff.txt lint doxygen
	@echo "[PASS] Compile/Execute/Compare"

.PHONY:
clean:
	@echo "Clean"
	@rm -f goto_test.diff.txt goto_test.this.txt goto_test goto_test.coverage
	@rm -f *.gcov *.gcda *.gcno *.lint

.PHONY:
doxygen: goto_test.h.cpp
	@echo "Doxygen"
	@doxygen $<
	@echo "TODO Fix the doxygen warnings"

.PHONY:
coverage: goto_test.h.cpp
	@echo "Coverage"
	@g++ --coverage -Wall -DLETTVIN_LEXERS_H_CPP_UNIT -o goto_test.coverage $<
	@./goto_test.coverage
	@gcov $< > $<.gcov

.PHONY:
lint: goto_test.h.cpp
	@cpplint $< > goto_test.lint 2>&1
	@echo "[PASS] Lint"

goto_test.diff.txt: goto_test.this.txt goto_test.pass.txt
	@echo "Compare $^"
	@diff $^ > $@

goto_test.this.txt:	goto_test
	@echo "Execute $@"
	@./$< | grep -v $(STARTS) | grep -v $(ENDS) > $@

goto_test:	goto_test.h.cpp
	@echo "Compile $@"
	@g++ -Wall -DLETTVIN_LEXERS_H_CPP_UNIT -o goto_test goto_test.h.cpp
