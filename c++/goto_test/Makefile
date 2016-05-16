#!/usr/bin/env make

STARTS="starts Basic style"
ENDS="ends Basic style"

all:	goto_test.diff.txt lint
	@echo "[PASS] Compile/Execute/Compare"

.PHONY:
clean:
	@echo "Clean"
	@rm goto_test.diff.txt goto_test.this.txt goto_test

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
