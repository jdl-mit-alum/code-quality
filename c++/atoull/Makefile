#!/usr/bin/env make

MODULE=atoull
COPTS=-std=c++11 -g -Wall -DLETTVIN_LEXERS_H_CPP_UNIT 
STEPS=0

all:	before coverage $(MODULE).diff.txt valgrind lint doxygen after
	@echo "[PASS] Compile/Execute/Compare"
	@echo "$(STEPS) steps finished"

.PHONY:
clean:
	@echo "\tMakefile: clean (removing files not members of deliverables)"
	@export STEPS="$(STEPS) + 1" | bc
	@rm -f $(MODULE).diff.txt $(MODULE).this.txt $(MODULE).pass.txt
	@rm -f $(MODULE) $(MODULE).coverage $(MODULE).doxygen.txt
	@rm -f *.gcov *.gcda *.gcno *.lint *.log *valgrind*
	@rm -fr *.dSYM

.PHONY:
before:
	@echo "\tMakefile: This Makefile runs in linux and Mac with gnu toolchain"
	@echo "\tMakefile: \tBeginning code quality checks"

.PHONY:
after:
	@echo "\tMakefile: Ending code quality checks."
	@echo "\tMakefile: \tMakefile finished without fatal error."
	@echo "\tMakefile: \tFinal report:"

.PHONY:
doxygen: Doxyfile $(MODULE).h.cpp
	@echo "\tMakefile: doxygen $@ (comment-to-documentation generator)"
	@doxygen > $(MODULE).doxygen.txt 2>&1
	@echo "[TODO] Fix the doxygen warnings"

.PHONY:
coverage: $(MODULE).h.cpp
	@echo "\tMakefile: coverage $@ (dead code identification)"
	@g++ --coverage $(COPTS) -o $(MODULE).coverage $<
	@./$(MODULE).coverage > /dev/null
	@gcov $< > $<.gcov

.PHONY:
lint: $(MODULE).h.cpp
	@echo "\tMakefile: lint $@ (static syntax check)"
	@cpplint $< > $(MODULE).lint 2>&1
	@echo "[PASS] Lint"

.PHONY:
valgrind: $(MODULE)
	@echo "\tMakefile: valgrind $(MODULE) (dynamic memory loss check)"
	@echo "\tMakefile: \t.valgrindrc contains command-line args"
	@echo "\tMakefile: \t$(MODULE).supp contains suppressions for libobjc and stdout errs"
	@echo "\tMakefile: \t\tsee http://www.valgrind.org/docs/manual/index.html"
	@valgrind -v --suppressions=$(MODULE).supp ./$< > /dev/null
	@echo "\tMakefile: \tvalgrind report\tsee http://www.valgrind.org/docs/manual/index.html"
	@# prevent Error (ignored) message from grep with || true
	@-tail -1 $(MODULE).valgrind | grep -v "0 errors from 0 contexts" || true

$(MODULE).diff.txt: $(MODULE).this.txt $(MODULE).pass.txt
	@echo "\tMakefile: diff $^ (output consistency check)"
	@diff -I atoull $^ > $@

$(MODULE).this.txt:	$(MODULE)
	@echo "\tMakefile: execute $@ (generate output for consistency check)"
	@./$< > $@

$(MODULE):	$(MODULE).h.cpp
	@echo "\tMakefile: compile $@ (create executable)"
	@g++ $(COPTS) -o $(MODULE) $(MODULE).h.cpp
