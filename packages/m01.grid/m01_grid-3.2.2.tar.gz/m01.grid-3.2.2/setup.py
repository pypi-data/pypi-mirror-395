##############################################################################
#
# Copyright (c) 2008 Projekt01 GmbH and Contributors.
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

from __future__ import absolute_import
#from __future__ import unicode_literals
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup (
    name='m01.grid',
    version='3.2.2',
    author = "Roger Ineichen, Projekt01 GmbH",
    author_email = "dev@projekt01.ch",
    description = "MongoDB grid file implementation for Zope3",
    long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    license = "ZPL 2.1",
    keywords = "Zope3 z3c p01 m01 mongo file grid",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    url = 'http://pypi.python.org/pypi/m01.grid',
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['m01'],
    extras_require=dict(
        test=[
            'm01.fake',
            'm01.stub',
            'zope.testing',
        ]),
    install_requires = [
        'setuptools',
        'm01.mongo',
        'pymongo',
        'z3c.form',
        'zope.component',
        'zope.contenttype',
        'zope.datetime',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.location',
        'zope.publisher',
        'zope.schema',
        'zope.security',
        'zope.site', # required by z3c.form latest
        ],
    zip_safe = False,
    )