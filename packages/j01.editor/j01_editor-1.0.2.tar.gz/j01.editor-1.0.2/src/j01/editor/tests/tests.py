###############################################################################
#
# Copyright (c) 2017 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Tests
$Id: tests.py 5752 2025-12-04 00:15:11Z roger.ineichen $
"""
from __future__ import absolute_import
from __future__ import print_function

import doctest
import unittest


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('checker.txt',
            globs={'print_function': print_function,
            # 'unicode_literals': unicode_literals,
            'absolute_import': absolute_import}
        ),
        doctest.DocFileSuite('util.txt',
            globs={'print_function': print_function,
            # 'unicode_literals': unicode_literals,
            'absolute_import': absolute_import},
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        ),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
