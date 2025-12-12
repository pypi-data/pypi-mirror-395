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
from builtins import str

import datetime

import zope.interface
import zope.component
import zope.datetime
import zope.publisher.browser
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces.http import IResult
from zope.security.proxy import removeSecurityProxy

from m01.grid import interfaces


def getFileResult(context, request, blocksize=32768):
    """Prepare a IFile result and apply header infos to response."""

    context = removeSecurityProxy(context)

    # set Content-Length
    request.response.setHeader('Content-Length', str(context.length))

    # set Content-Type
    request.response.setHeader('Content-Type', context.contentType)

    # set Last-Modified
    modified = context.uploadDate

    if modified is not None and isinstance(modified, datetime.datetime):
        lmt = zope.datetime.time(modified.isoformat())

        # return cache header if asked for and no newer data available
        header = request.getHeader('If-Modified-Since', None)
        if header is not None:
            header = header.split(';')[0]
            try:
                mod_since = int(zope.datetime.time(header))
            except:
                mod_since = None
            if mod_since is not None and lmt <= mod_since:
                request.response.setStatus(304)
                return ''

        request.response.setHeader('Last-Modified', 
            zope.datetime.rfc1123_date(lmt))

    # get the file chunk reader which acts as an open file in read mode
    chunkReader = interfaces.IChunkReader(context)

    # wrap our IFileReader into the given wrapper
    wrapper = request.environment.get('wsgi.file_wrapper', None)
    if wrapper is not None:
        return wrapper(chunkReader, chunkReader.readBlockSize)

    # return our file chunk reader adapter
    return chunkReader


@zope.component.adapter(interfaces.IFile, IHTTPRequest)
@zope.interface.implementer(IResult)
def FileResult(context, request):
    """Provides a IResult if we directly return a IFile as result."""
    return getFileResult(context, request)


class FileDownload(zope.publisher.browser.BrowserPage):
    """Download view for IFile."""

    blocksize = 32768

    def getFile(self):
        return self.context

    def __call__(self):
        """Supports data download."""
        context = self.getFile()
        # get an IResult for IFile. We could also return the IFile here, but
        # this whould end in calling the IResult adapter for (IFile, request)
        return getFileResult(context, self.request, self.blocksize)