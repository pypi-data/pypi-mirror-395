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
from __future__ import absolute_import

import zope.i18nmessageid
import zope.schema.interfaces

from pymongo.errors import PyMongoError

_ = zope.i18nmessageid.MessageFactory('p01')


class FileError(PyMongoError):
    __doc__ = _("""File upload exceptions""")


class CorruptFile(FileError):
    __doc__ = _("""Malformed file upload""")


class TooLargeFile(FileError):
    __doc__ = _("""Too large file given""")


class MissingFileNameExtension(zope.schema.interfaces.ValidationError):
    __doc__ = _("""Missing filename extension""")


class AllowedFormatError(zope.schema.interfaces.ValidationError):
    __doc__ = _("""Not allowed file format""")