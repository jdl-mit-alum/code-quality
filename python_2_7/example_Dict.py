#!/usr/bin/env python

#   pep8 --ignore=E272,E203,E202,E221 test_Dict.py

# pragma pylint: disable=invalid-name
# pragma pylint: disable=bad-whitespace

#   pyflakes test_Dict.py
# This still reports "imported but unused"

"""example_Dict.py

Usage:
    example_Dict.py \
[(-c<Hues>|--color=<Hues>)]\
[(-v|--verbose)]\
[(-w<W>|--width=<W>)]
    example_Dict.py (-h | --help)
    example_Dict.py (--version)

Options:
    -c <Color>, --color=<Color>     color   for string test [default: rg]
    -w <Width>, --width=<Width>     width   for number test [default: 13]
    -v, --verbose                   verbose for bool   test [default: False]
    -h --help                       Show this screen
    --version                       Show version

Author: Jonathan D. Lettvin
LinkedIn: jlettvin
Date: 20160512
"""

from docopt import (docopt)

from python_2_7.Dict import (Dict)


def example(easy, **hard):
    """
    The example function exercises the two access methods (dict vs. Dict).
    Compare the syntax of easy (Dict) vs. hard (dict).
    """

    # Here you can see the syntax difference for a simple assignment.
    easy.color = "by"
    hard["--color"] = "by"

    # Here you can see the syntax difference for a bulk update.
    values = {'update': 3.14159, 'weekday': 'MTWRF'}
    easy(**values)
    hard.update(values)

    # Here we examine the contents for simple visual comparison.
    print "[string]? '%s' == '%s'" % (easy.color  , hard["--color"  ])
    print "[  bool]? '%s' == '%s'" % (easy.verbose, hard["--verbose"])
    print "[number]? '%f' == '%f'" % (easy.update , hard["update"   ])
    print "[string]? '%s' == '%s'" % (easy.weekday, hard["weekday"  ])

    assert easy.color   == hard["--color"]  , "Compare strings"
    assert easy.verbose == hard["--verbose"], "Compare    bool"
    assert easy.update  == hard["--update"] , "Compare numbers"
    assert easy.weekday == hard["--weekday"], "Compare strings"


if __name__ == "__main__":

    def main():
        "main is the traditional module entrypoint"

        kwargs = docopt(__doc__, version="0.0.1")
        Args   = Dict(**kwargs)

        example(Args, **kwargs)

    main()
