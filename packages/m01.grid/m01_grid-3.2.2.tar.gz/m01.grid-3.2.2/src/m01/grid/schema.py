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
#from __future__ import unicode_literals
from zope.interface import implementer

import zope.interface
import zope.schema
import zope.schema.interfaces
import zope.i18nmessageid

import m01.grid.exceptions

_ = zope.i18nmessageid.MessageFactory('p01')


def getCleanFileName(filename):
    """Strip path from filenme (could happen in IE)"""
    cleanFileName = filename.split('\\')[-1]
    return cleanFileName.split('/')[-1]

def validateFileNameExtension(fileName):
    """Stip out path in filename (happens in IE upload)"""
    # strip out the path section even if we do not remove them
    # later, because we just need to check the filename extension.
    dottedParts = fileName.split('.')
    if len(dottedParts) <= 1:
        raise m01.grid.exceptions.MissingFileNameExtension()

def validateAllowedFormat(fileName, allowedFormats):
    if not '*' in allowedFormats:
        postfix = fileName.split('.')[-1].lower()
        if postfix not in allowedFormats:
            v = _('Files ending with "$postfix" are not allowed.',
                  mapping={'postfix': postfix})
            raise m01.grid.exceptions.AllowedFormatError(fileName)


# IFile upload schema field
class IFileUpload(zope.schema.interfaces.IField):
    """File upload field interface."""

    minSize = zope.schema.Int(
        title=_(u'Minimum file size'),
        description=_(u'Minimum file size'),
        min=0,
        required=False,
        default=None)

    maxSize = zope.schema.Int(
        title=_(u'Maximum file size'),
        description=_(u'Maximum file size'),
        min=0,
        required=False,
        default=None)

    allowedFormats = zope.schema.Tuple(
        title=_(u'Allowed Formats'),
        description=_(u'Allowed Formats'),
        default=(u'*',),
        required=True)


@implementer(IFileUpload)
class FileUpload(zope.schema.Field):
    """File upload field implementation."""


    def __init__(self, allowedFormats='*', minSize=0, maxSize=None, **kw):
        self.allowedFormats = allowedFormats
        self.minSize = minSize
        self.maxSize = maxSize
        super(FileUpload, self).__init__(**kw)

#    def validateFileName(self, filename):
#        # get file extension
#        dottedParts = filename.split('.')
#        if len(dottedParts) <= 1:
#            raise m01.grid.exceptions.MissingFileNameExtension(filename)
#        if not '*' in self.allowedFormats:
#            postfix = filename.split('.')[-1].lower()
#            if postfix not in self.allowedFormats:
#                v = _('Files ending with "$postfix" are not allowed.',
#                      mapping={'postfix': postfix})
#                raise m01.grid.exceptions.AllowedFormatError(filename)

    def _validate(self, value):
        super(FileUpload, self)._validate(value)

        # strip out the path section
        cleanFileName = getCleanFileName(value.filename)

        # validate filename extension
        validateFileNameExtension(cleanFileName)

        # validate allowed extension
        validateAllowedFormat(cleanFileName, self.allowedFormats)

#        # we will validate the file size in ChunkWriter because we don't like
#        # to load the item into memory by reading the size
#        # validate size if given
#        if self.minSize is not None and value.size < self.minSize:
#            raise zope.schema.interfaces.TooSmall(value, self.minSize)
#
#        if self.maxSize is not None and value.size > self.maxSize:
#            raise zope.schema.interfaces.TooBig(value, self.maxSize)