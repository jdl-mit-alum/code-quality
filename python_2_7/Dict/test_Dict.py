#!/usr/bin/env python

#   pep8 --ignore=E272 test_Dict.py

# pragma pylint: disable=invalid-name
# pragma pylint: disable=too-few-public-methods
# pragma pylint: disable=unused-argument
# pragma pylint: disable=unused-import
# pragma pylint: disable=wrong-import-position
# pragma pylint: disable=wrong-import-order
# pragma pylint: disable=eval-used
# pragma pylint: disable=pointless-statement
# pragma pylint: disable=relative-import
# pragma pylint: disable=bare-except

#   pyflakes test_Dict.py
# This still reports "imported but unused"

# Section 1 -------------------------------------------------------------------
"""test_Dict.py

Usage:
    test_Dict.py \
[(-c<Hues>|--color=<Hues>)]\
[(-v|--verbose)]\
[(-e|--coverage)]\
[(-w<W>|--width=<W>)]
    test_Dict.py (-h | --help)
    test_Dict.py (--version)

Options:
    -c <Color>, --color=<Color>     Print colors for pass/fail [default:"00"]
    -w <Width>, --width=<Width>     Print width of conclusion [default:79]
    -v, --verbose                   Show execution details [default: False]
    -h --help                       Show this screen
    --version                       Show version

This module is designed as a teaching exercise.
Although the new Dict class is operational and servicable
it is not necessarily complete and matured for all possible uses.

<Color> is expected to be a pair from the set '0rgybmcw':
    0: black  r: red      g: green  y: yellow
    b: blue   m: magenta  c: cyan   w: white
    where the first color is used for FAIL and the second for PASS
    against the current default background color.
    (i.e. --color=rg makes FAIL appear in red and PASS appear in green).
    If not given on the command-line or set to "00",
    no ANSI color formatting is used, to enable text editor review of output.
    http://en.wikipedia.org/wiki/ANSI_escape_code

Example:
    ./test_Dict.py --color=rg

Author: Jonathan D. Lettvin
LinkedIn: jlettvin
Date: 20141020

Modified: 20160512 for Altman Vilandrie example of Code Quality.
"""

from types import (MethodType)

# This bizarre stacked try/except clause is used to bypass an error in coverage
# where imports through __init__.py are improperly handled.
# pylint disables relative-import and bare-except are required to silence them.
try:
    from Dict import (Dict)
except:
    try:
        from Dict import (Dict)
        assert False, 'Force coverage'
    except:
        pass  # bypass coverage bug


class Compare(object):
    """
    This class presents a singleton functor and conclusion interface.
    The functor compares pairs of adjacent objects expecting equality.
    The conclusion prints the result of all preceding functor compares
    in a clean and easy-to-scan review format.
    This class provides limited local unit test support to avoid
    command-line argument parsing conflict between the libraries named
    unittest2 and docopt.
    ANSI colors may be used to enhance unit test output via command-line args.
    """

    Width, Pass, Fail, Verbose, Text, Color = 79, 0, 0, True, [], "00"
    colorList = {k: n for n, k in enumerate('0rgybmcw')}
    ANSIformat = '\x1b\x5b3%sm'
    COLOR = [ANSIformat % (hue) for hue in (0, 0, 0)]
    RESET = '\x1b\x5b31;0m'

    @staticmethod
    def _recolor(index, hue):
        "Update ANSI sequences for output"
        assert 0 <= index <= 1 and 0 <= hue <= 7
        Compare.COLOR[index] = Compare.ANSIformat % (hue)

    @staticmethod
    def __call__(msg, *args, **kw):
        """
        This functor compares adjacent pairs of objects in its arg list.
        args is a list of objects to compare.
        kw is the key:value pairs from the docopt command-line dictionary.
        If there is no pair, the message is added without compares.
        """
        Compare.Verbose = kw.get('--verbose', Compare.Verbose)
        Compare.Width = kw.get('--width', Compare.Width)
        # Update ANSI color usage if default and proposed on command-line.
        if Compare.Color == "00":
            # This conditional handles deferred command-line arg handling.
            if '--color' in kw.keys():
                color = kw.get('--color', Compare.Color)
                Compare.Color = color if color else Compare.Color
                assert len(Compare.Color) == 2
                assert all([h in Compare.colorList for h in Compare.Color])
            for index, char in enumerate(Compare.Color):
                assert char in Compare.colorList.keys()
                color = Compare.colorList[char]
                Compare._recolor(index, Compare.colorList[char])
        # Update width of output if proposed on command-line.
        Compare.Width = int(Compare.Width if Compare.Width else 79)
        if not args:
            # Add message without PASS/FAIL if args are absent.
            if Compare.Verbose:
                Compare.Text.append([False, '       %s' % (msg)])
            return
        else:
            # Compare args if present and indicate PASS/FAIL
            try:
                largs = list(args)
                assert all([(b == c) for b, c in zip(largs[:-1], largs[1:])])
                Compare.Text.append([True, '%(PASS)s ' + msg])
                Compare.Pass += 1
                assert kw.get('--coverage', False), 'Force coverage'
            except AssertionError:
                Compare.Text.append([True, '%(FAIL)s ' + msg])
                Compare.Fail += 1
        for arg in args:
            # Add display of tested args if --verbose
            Compare.Text.append([False, arg])

    @staticmethod
    def conclusion():
        "This method assembles a report into a printable form."

        def rule(retval, **kw):
            "This function makes a horizontal line with a title (if given)."
            msg, char = (kw.get(k, v) for k, v in [('msg', ''), ('char', '-')])
            msg = ' %s ' % (msg) if msg else char * 2
            retval += char * 6 + msg
            retval += char * (Compare.Width - len(msg) - 6) + '\n'
            return retval

        # Start with a horizontal line.
        retval = rule('', msg='INDIVIDUAL')
        # Loop through accumulated proposed outputs.
        for show, text in Compare.Text:
            if not Compare.Verbose:
                if show:
                    retval += '%s\n' % (text)
            else:
                retval += '%s\n' % str(text)
        # Add another horizontal line.
        retval = rule(retval, msg='SUMMARY')
        # Add summaries of PASS/FAIL counts and REVIEW flag if FAILS.
        review = '   REVIEW!' if Compare.Fail else ''
        retval += '%(PASS)s' + ' count = %d\n' % (Compare.Pass)
        retval += '%(FAIL)s' + ' count = %d %s\n' % (Compare.Fail, review)
        # Add a final horizontal line with a timestamp.
        import datetime
        retval = rule(retval, msg=datetime.datetime.now())
        # Setup string formatting to substitute ANSI colors where proposed.
        failpass = ['[FAIL]', '[PASS]']
        if Compare.Color != "00":
            failpass = [
                Compare.COLOR[i] + failpass[i] + Compare.RESET
                for i in range(2)]
        # Use string formatting to substitute ANSI colors where proposed.
        return retval % {'FAIL': failpass[False], 'PASS': failpass[True]}

# Create a compare singleton instance to hold unit test results.
# Use it to declare the previous section immediately.
REPORT = Compare()
REPORT('Section 1   docopt and unit test setup')

REPORT('Section 2   definition of Dict class')
# Section 2 -------------------------------------------------------------------

REPORT('Section 3   definition of unit test function')
# Section 3 -------------------------------------------------------------------


def test_0000(**kw):
    """
    This function is the typically named unit test entry point.
    Numbered subtest functions are defined which return pairs of objects
    which are supposed to compare as equal.
    A dictionary at the bottom collects and names the subtests.
    A function named 'act' executes a single test with further labeling.
    A loop marches through the dictionary executing the tests with 'act'.
    """

    def testfunction0():
        "Compare after default initialization."
        return (Dict(), dict())  # Does new class compare to encapsulated one?

    def testfunction1():
        "Compare after standard initialization."
        return (Dict(a=1, b=2), dict(a=1, b=2))  # How about initialized?

    def testfunction2():
        "Compare after lexical access on new class."
        dict1, dict2 = dicts12 = (Dict(a=1, b=2), dict(a=1, b=2))
        dict1.a = 3
        dict2['a'] = 3
        return dicts12  # How about updated after initialized?

    def testfunction3():
        "Compare after new class updating method."
        dict1, dict2 = dicts12 = (Dict(a=1, b=2), dict(a=1, b=2))
        dict1.let(a=5, b=6, c=-1)
        dict2.update({'a': 5, 'b': 6, 'c': -1})
        return dicts12  # How about bulk updating?

    def testfunction4():
        "Check new class acts like standard dict."
        dict1, dict2 = dicts12 = (Dict(a=1, b=2), dict(a=1, b=2))
        dict1.update({'a': 7, 'b': 8, 'c': -2, 'd': -3})
        dict2.update({'a': 7, 'b': 8, 'c': -2, 'd': -3})
        return dicts12  # How about old-style updating on new class?

    def testfunction5():
        "Compare lexical and keyword accessing."
        dict1, dict2 = dicts12 = (Dict(), dict())
        dict1.hello = 'hello world'
        dict2['hello'] = 'hello world'
        return dicts12  # How about adding lexically vs. dictionary?

    def testfunction6():
        "Compare converting command-line arguments."
        converted = {k.replace('-', ''): v for k, v in kw.items()}
        dicts12 = (Dict(**kw), dict(**converted))
        return dicts12  # How about command-line args with '-' characters?

    def testfunction7():
        "Compare execution after method attachment."
        def cogito(self, msg):
            "This function will be converted to a method in both dictionaries."
            return '%s %s' % (therefore, msg)
        therefore, exist = 'ergo', 'sum'
        dict1, dict2 = Dict(), Dict()
        dict1.Ithink = MethodType(cogito, dict1, Dict)
        dict2.method(Ithink=cogito)
        string0 = ' '.join([therefore, exist])
        string1, string2 = dict1.Ithink(exist), dict2.Ithink(exist)
        return (string0, string1, string2)  # How about adding a method?

    def testfunction8():
        "Use __call__"
        dict1, dict2 = dicts12 = (Dict(a=1, b=2), dict(a=1, b=2))
        dict1(a=5, b=6, c=-1)
        dict2.update({'a': 5, 'b': 6, 'c': -1})
        return dicts12  # How about bulk updating?

    def act(msg, fun):
        "Run compare function on test function results."
        REPORT('Section 6.%s %s' % (msg, fun.__doc__), *fun())

    # Here is a dictionary of labelled test functions to run.
    test = {'0: empty dictionary': testfunction0,
            '1: initialized vals': testfunction1,
            '2: separate updates': testfunction2,
            '3: bulk data update': testfunction3,
            '4: old styles works': testfunction4,
            '5: lexical updating': testfunction5,
            '6: command-line arg': testfunction6,
            '7: attached methods': testfunction7,
            '8: __call__ updates': testfunction8, }

    # Here is a loop to execute al the labelled test functions.
    for key in sorted(test.keys()):
        act(key, test[key])

# Section 4 -------------------------------------------------------------------
if __name__ == "__main__":
    REPORT('Section 4   entering __main__ section')
    from sys    import (version_info)  # NOQA
    from docopt import (docopt)

# Section 5 -------------------------------------------------------------------
    REPORT('Section 4.1 defining main() function to setup/run unit test')

    def main():
        """
        This is the root of execution.
        When executed from the command-line, this section is the entry-point.
        http://docopt.org/
        """
        REPORT('Section 5   running main()')
        kwargs = docopt(__doc__, version="0.0.1")
        REPORT('Section 5.1 set verbosity flag', **kwargs)
        REPORT('Section 5.2 check coverage 1',
               (kwargs.get('--coverage') is False),
               **kwargs)
        REPORT('Section 5.3 check python version',
               (version_info.major == 2 and version_info.minor == 7),
               **kwargs)
        test_0000(**kwargs)
        print REPORT.conclusion()

# Section 6 -------------------------------------------------------------------
    REPORT('Section 4.2 execute main and display unit test final result')
    main()
