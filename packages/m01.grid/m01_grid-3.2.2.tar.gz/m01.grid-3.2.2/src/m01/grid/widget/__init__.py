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
from zope.interface import implementer_only

import zope.interface
import zope.component

from z3c.form import widget
import z3c.form.browser.file
from z3c.form.interfaces import IFieldWidget

import m01.grid.schema
import m01.grid.layer
from m01.grid import interfaces


# z3c.from
@implementer_only(interfaces.IFileUploadWidget)
class FileUploadWidget(z3c.form.browser.file.FileWidget):
    """Widget for IFileUpload field.

    The registered FileUploadDataConverter for this widget returns an
    FileUpload item
    """


    css = u'gridFileUploadWidget'


@zope.component.adapter(m01.grid.schema.IFileUpload,
                        m01.grid.layer.IFileUploadWidgetLayer)
@zope.interface.implementer(IFieldWidget)
def FileUploadFieldWidget(field, request):
    """IFieldWidget factory for FileUploadWidget."""
    return widget.FieldWidget(field, FileUploadWidget(request))