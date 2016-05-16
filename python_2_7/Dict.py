#!/usr/bin/env python

#   pep8 --ignore=E721 Dict.py
# pragma pylint: disable=invalid-name
# pragma pylint: disable=no-member
# pragma pylint: disable=wrong-import-position

"""Dict.py
Author: Jonathan D. Lettvin
LinkedIn: jlettvin
Date: 20141020

This module implements the ability to substitute
member names for explicit dictionary dereferences.

    hard = {'hello': 'world', 'a': 'b'}
    easy = Dict(**source)

    assert easy.hello == hard['hello'], "This error never happens"
    hard['hello'] = 'monde';
    easy.hello    = 'monde'
    assert easy.hello == hard['hello'], "This error never happens"

See test_Dict.py to see the implemented methods and usage patterns available.
"""

from types import (MethodType)


class Dict(dict):
    """
    This derived class adds the ability to view and modify a dictionary
    using the simpler lexical naming convention used for code token names
    rather than the more complex braces and quotes dictionary accessors.
    """

    remove = '-<>'  # Add characters to this string to get them removed.

    @staticmethod
    def _clean(k):
        """
        This private method removes non-token characters from strings.
        Remove all '-' characters from hashable key to make it lexically ok,
        for instance when converting argv command-line dicts.
        https://docs.python.org/2/library/string.html#string.translate
        """
        return k.translate(None, Dict.remove)

    def _method(self, value):
        """
        This private method converts external functions to internal methods.
        https://docs.python.org/2/library/types.html

        Comparing types is considered unidiomatic, but it is necessary here.
        To avoid a pylint error, they are assigned to variables before assert.
        """
        vtype, dtype = type(value), type(Dict._clean)
        assert dtype == vtype
        return MethodType(value, self, Dict)

    def __init__(self, **kw):
        """
        __class__ has a __dict__ member.
        By replacing this __dict__ member with the parent dict builtin
        we may access its members lexically instead of with hashable keys.
        """
        super(Dict, self).__init__()        # NOOP to prevent pylint error
        self.__dict__ = self                # This is the magic line
        self.let(**kw)

    def __call__(self, **kw):
        'Update the instance dictionary'
        self.let(**kw)
        return self

    def let(self, **kw):
        "instance dictionary bulk updater"
        self.update({Dict._clean(k): v for k, v in kw.items()})
        return self

    def method(self, **kw):
        "instance dictionary bulk method attacher"
        self.update({Dict._clean(k): self._method(v) for k, v in kw.items()})
        return self

if __name__ == "__main__":

    import sys

    def main():
        "Sample run."

        harder = {'hello': 'world'}
        easier = Dict(**harder)

        try:
            assert easier.hello == harder["hello"], 'Test failed'
            assert len(sys.argv) == 1, 'No command line args permitted'
            print '[PASS] ' + __file__ + ' Sample worked'
        except AssertionError:
            print '[FAIL] ' + __file__ + ' Sample failed'

    main()
