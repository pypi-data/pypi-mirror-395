###############################################################################
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
###############################################################################
"""
$Id:$
"""
from __future__ import absolute_import
from builtins import object

import m01.mongo.base
from m01.mongo.fieldproperty import MongoFieldProperty

from m01.grid import interfaces
import m01.grid.chunker


class FileBase(object):
    """File base class"""

    chunkSize = MongoFieldProperty(interfaces.IFile['chunkSize'])
    numChunks = MongoFieldProperty(interfaces.IFile['numChunks'])
    md5 = MongoFieldProperty(interfaces.IFile['md5'])
    uploadDate = MongoFieldProperty(interfaces.IFile['uploadDate'])

    filename = MongoFieldProperty(interfaces.IFile['filename'])
    length = MongoFieldProperty(interfaces.IFile['length'])
    contentType = MongoFieldProperty(interfaces.IFile['contentType'])
    encoding = MongoFieldProperty(interfaces.IFile['encoding'])

    removed = MongoFieldProperty(interfaces.IFile['removed'])

    # not stored in mongo
    maxFileSize = interfaces.MAX_FILE_SIZE

    @property
    def chunkCollection(self):
        """Returns a mongodb collection for store file chunks.

        IMPORTANT:

          The chunkCollection MUST provide a compound index for files_id and n

        You can setup such an index with pymongo ensure_index like:

          chunkCollection.ensure_index(
            [("files_id", ASCENDING), ("n", ASCENDING)], unique=True)

        You need to provide 2 collections with the following rules.

        The file item collection must end with ``.files`` and the chunks
        collection must end with ``.chunks``. Both collections must provide
        the same namespace. Each GridFS driver uses ``fs`` as the default
        namepace e.g. fs.files and fs.chunks. It is also possible to use an own
        namspace e.g. doc.files and doc.chunks.

        """
        raise NotImplementedError(
            "Subclass must implement the chunkCollection attribute")

    def getFileWriter(self):
        """Returns a IChunkReader"""
        return m01.grid.chunker.ChunkWriter(self)

    def getFileReader(self):
        """Returns a IChunkReader"""
        return m01.grid.chunker.ChunkReader(self)

    def applyFileUpload(self, fileUpload):
        """Apply FileUpload given from request publisher"""
        if not fileUpload or not fileUpload.filename:
            # empty string or None means no upload
            raise ValueError("Missing file upload data")
        elif self.removed:
            raise ValueError("Can't store data for removed files")
        writer = self.getFileWriter()
        writer.add(fileUpload)

    @property
    def size(self):
        return self.length

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.__name__)


class FileItemBase(FileBase, m01.mongo.base.MongoItemBase):
    """Mongo file item base class."""

    _dumpNames = ['_id', '_pid', '_type', '_version', '__name__',
                  'created', 'modified', 'removed',
                  'chunkSize', 'numChunks', 'md5', 'uploadDate',
                  'filename', 'length', 'contentType', 'encoding']

    def notifyRemove(self):
        writer = self.getFileWriter()
        writer.remove()


class SecureFileItemBase(FileBase, m01.mongo.base.SecureMongoItemBase):
    """Secure mongo file item base class."""

    _dumpNames = ['_id', '_pid', '_type', '_version', '__name__',
                  'created', 'modified', 'removed',
                  '_ppmrow', '_ppmcol',
                  '_prmrow', '_prmcol',
                  '_rpmrow', '_rpmcol',
                  'chunkSize', 'numChunks', 'md5', 'uploadDate',
                  'filename', 'length', 'contentType', 'encoding']

    def notifyRemove(self):
        writer = self.getFileWriter()
        writer.remove()