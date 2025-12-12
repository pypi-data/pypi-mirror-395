##############################################################################
#
# Copyright (c) 2011 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id:$
"""
__docformat__ = "reStructuredText"

import doctest
import unittest

import m01.grid.testing
import six

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('README.txt', encoding='utf8',
            setUp=m01.grid.testing.setUpStubMongo,
            tearDown=m01.grid.testing.tearDownStubMongo,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        ),
        doctest.DocFileSuite('gridfs.txt', encoding='utf8',
            setUp=m01.grid.testing.setUpStubMongo,
            tearDown=m01.grid.testing.tearDownStubMongo,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        ),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
