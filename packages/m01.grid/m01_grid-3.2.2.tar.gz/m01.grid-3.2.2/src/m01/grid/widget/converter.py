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

import zope.component
import zope.i18nmessageid
import zope.publisher.browser

import z3c.form.interfaces
from z3c.form.converter import BaseDataConverter

import m01.grid.schema

_ = zope.i18nmessageid.MessageFactory('p01')


class FileUploadDataConverter(BaseDataConverter):
    """A special data converter for IFileUpload

    This converter simply returns the FileUpload which wraps the tmp file
    
    This prevents to load the data inot memory and we can process them later in
    our grid storage

    """
    zope.component.adapts(m01.grid.schema.IFileUpload,
        z3c.form.interfaces.IWidget)

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        # ignore existing data, there is no need for display them
        return u''

    def toFieldValue(self, value):
        """See interfaces.IDataConverter
        
        We should allways get a FileUpload object. Don't load the data  into 
        the memory, just return the FileUpload and process the referenced file
        later in ChunkWriter.
        
        We validate here because we like to prevent to write bad data to the
        chunks collection.

        """
        if value is None or value == '':
            # When no new file is uploaded, send a signal that we do not want
            # to do anything special.
            return z3c.form.interfaces.NOT_CHANGED

        elif isinstance(value, zope.publisher.browser.FileUpload):
            # make the following attributes available in widget
            self.widget.headers = value.headers
            # get filename and return missing_value if empty
            filename = getattr(value, 'filename', '')
            if not filename:
                return self.field.missing_value

            # strip path from filename (could happen in IE)
            cleanFileName = m01.grid.schema.getCleanFileName(filename)
            # validate filename extension
            m01.grid.schema.validateFileNameExtension(cleanFileName)
            # validate allowed formats
            m01.grid.schema.validateAllowedFormat(cleanFileName,
                self.field.allowedFormats)
            self.widget.filename = cleanFileName
            return value
        else:
            # should never happen
            raise ValueError(_(u'No FileUpload given.'))