# Examples of medium/high quality C++ projects

## atoull 
This implements a robust high-performance string to unsigned long long convert.

## tenpin
This implements scoring/errors/exceptions for tenpin bowling games.

## Principles

Features of quality include:
* Strong use of comments
* Comments for use of doxygen to produce module documentation
* Header comment for module comprehension
* Visual cue comments for rapid scanning by eye
* Explanation comments for unit tests and their goals
* 100% Syntax compliance with lint
* Allowable naming conventions for libraries, classes, methods, members
* 100% Code coverage
* Comparison with known valid output
* [PASS]/[FAIL] visual cues for issues
* Cleanup to the minimum set of sources
* No dead code

### Comments

Comments add value in many ways:
* Identify author/organization/history/legal
* Explain what the goal of the code is (problem i.e. input/transform/output)
* Explain how the goal is achieved (solution)
* Reference literature on solution (possible alternatives)
* Describe merits of solution choice (simplicity/maintainability/efficiency)
* Explain non-obvious or off-standard coding techniques (i.e. computed goto)
* List environments where results have been tested (OS/version/chip/compiler)
* Identify architecture/compiler/platform limitations
* Example compile instructions
* Describe how to run tests
* Identify conventions followed
* Specifically identify interfaces (call signatures)
* Mark quality control exceptions (NOLINT/pragma pylint)
* Provide data for automatic document generators (doxygen)
* Visual assistance for navigating the source
* Describe limitations and directions for future development (todo)
* Illustrate usage with a variety of examples
* Identify name overloading and explain why name re-use was chosen

### Syntax compliance
* Identify tool(s) used (lint/pep8/pylint/pyflakes)
* Achieve and document 100% compliance
* Document exceptions and reasons for exceptions
* Identify standard for compliance (pep8/pep20/google c++ style guide)
* Explain choice for deviation from standard

### Naming conventions
* Identify standard (pep20/google c++ style guide)
* Explain deviation from standard

### Example valid inputs/outputs
* Examples of typical use
* Examples of "edge/corner" cases illustrating input/output limitations

### Unit testing/coverage
* Identify where unit tests are stored
* Describe how unit tests are run
* Set expectations for elapsed time and results
* Aid testing with clear identification of test PASS/FAIL results
* Identify artifact storage location
* Store artifacts
* Keep example expected output for comparison
* Compare expected output with actual output
* Identify problematic differences between expected/actual output

### Automatically generate documentation
* Identify tool (doxygen/pydoc)
* Identify artifact storage location
* Generate and store documentation into artifact
* Document quality process in documentation root (README.md/index.html)

### Resource problems
* Describe memory leaks or garbage accumulation (valgrind)
