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
$Id: traverser.py 5233 2025-04-18 13:16:38Z rodrigo.ristow $
"""
from __future__ import absolute_import
#from __future__ import unicode_literals

import zope.interface
import zope.publisher.interfaces
import zope.publisher.interfaces.browser
import m01.grid.browser


class FileObjectByFileNameTraverser(zope.location.location.Location):
    """Dummy context for FileObject offering the filename as traversable view.

    This traverser allows us to traverse the FileObject item by it's filename

    Note: this traverser is not registered by default. You need to register
    this traverser in your application with the correct permission for your
    own FileObject implementations.

    """

    zope.interface.implements(
        zope.publisher.interfaces.browser.IBrowserPublisher)

    def __init__(self, context, request):
        if context is None:
            # raise error if FielObject is None
            raise zope.publisher.interfaces.NotFound(context, u'', request)
        self.context = context
        self.request = request
        self.__parent__ = context
        self.__name__ = context.filename

    def publishTraverse(self, request, name):
        """Allows to traverse the FileObject with the real filename without 
        to register a named view.
        """
        if name == self.context.filename:
            view = m01.grid.browser.FileDownload(self.context, self.request)
            view.__name__ = name
            return view
        raise zope.publisher.interfaces.NotFound(self, name, request)