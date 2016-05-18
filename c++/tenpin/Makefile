#!/usr/bin/env make

MODULE=tenpin





all: coverage $(MODULE).diff.txt lint doxygen

.PHONY:
clean:
	@echo "Clean"
	@rm -f $(MODULE).this.txt $(MODULE).diff.txt
	@rm -f $(MODULE) $(MODULE).coverage $(MODULE).doxygen.txt
	@rm -f *.gcov *.gcda *.gcno *.lint

.PHONY:
doxygen: $(MODULE).doxygen.config $(MODULE).cpp
	@echo "Doxygen"
	@doxygen $< > $(MODULE).doxygen.txt 2>&1
	@echo "[TODO] Fix the doxygen warnings"

.PHONY:
coverage: $(MODULE).cpp
	@echo "Coverage"
	@g++ --coverage -Wall -DLETTVIN_LEXERS_H_CPP_UNIT -o $(MODULE).coverage $<
	@./$(MODULE).coverage
	@gcov $< > $<.gcov

.PHONY:
lint: $(MODULE).cpp
	@cpplint $< > $(MODULE).lint 2>&1
	@echo "[PASS] Lint"

$(MODULE).diff.txt: $(MODULE).this.txt $(MODULE).pass.txt
	@echo "Compare $^"
	@diff $^ > $@

$(MODULE).this.txt: $(MODULE) Makefile
	@echo "Execute $@"
	./$(MODULE) > $(MODULE).this.txt 2>&1

$(MODULE): $(MODULE).cpp Makefile
	@echo "Compile $@"
	g++ -Wall -o $@ $<
