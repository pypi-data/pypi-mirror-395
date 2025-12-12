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
from __future__ import division
from future import standard_library

standard_library.install_aliases()

import six
from builtins import object
from past.utils import old_div

__docformat__ = "reStructuredText"

import sys
import datetime
import hashlib
import logging
import math
import os
from io import BytesIO

try:
    basestring              # p01.checker.silence
except NameError:
    basestring = str        # p01.checker.silence
try:
    unicode                 # p01.checker.silence
except Exception:
    unicode = str           # p01.checker.silence

import bson.binary
import pymongo.errors
import pymongo.write_concern

import zope.interface
from zope.contenttype import guess_content_type

from m01.mongo import UTC

import m01.grid.exceptions
from m01.grid import interfaces


logger = logging.getLogger('m01.grid')

_SEEK_SET = os.SEEK_SET
_SEEK_CUR = os.SEEK_CUR
_SEEK_END = os.SEEK_END


###############################################################################
#
# convert text to binary

try:
    import chardet
    HAS_CHARDET = hasattr(chardet, 'detect')
except ImportError:
    HAS_CHARDET = False

PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes

FALLBACK_ENCODINGS = ['utf-8', 'latin-1', 'cp1252']

def ensure_utf8_bytes(data):
    """
    Konvertiert beliebigen Text oder Bytes sicher in UTF-8-codierte Bytes.

    :param data: str, unicode oder bytes
    :return: bytes (UTF-8)
    :raises: TypeError, ValueError
    """
    if data is None:
        return b''

    if isinstance(data, text_type):
        return data.encode('utf-8')

    # Convert to memoryview if needed
    elif isinstance(data, memoryview):
        return bytes(data)

    elif isinstance(data, bson.binary.Binary):
        return bytes(data)

    elif isinstance(data, binary_type):
        try:
            data.decode('utf-8')
            return data
        except UnicodeDecodeError:
            pass
        enc = None
        if HAS_CHARDET:
            result = chardet.detect(data)
            enc = result.get('encoding')
            confidence = result.get('confidence', 0) or 0
            if not enc or confidence < 0.5:
                enc = None
        tried_encodings = set()
        for en in [enc] + FALLBACK_ENCODINGS:
            if not en or en in tried_encodings:
                continue
            tried_encodings.add(en)
            try:
                return data.decode(en).encode('utf-8')
            except Exception:
                continue
        raise ValueError(
            "Could not convert data to UTF-8: unknown encoding or corrupt input.")

    else:
        raise TypeError("Input must be text or bytes, got: %r" % type(data))


def extractFileName(filename):
    """Stip out path in filename (happens in IE upload)"""
    # strip out the path section even if we do not remove them
    # later, because we just need to check the filename extension.
    cleanFileName = filename.split('\\')[-1]
    cleanFileName = cleanFileName.split('/')[-1]
    dottedParts = cleanFileName.split('.')
    if len(dottedParts) <= 1:
        raise m01.grid.exceptions.MissingFileNameExtension()
    return cleanFileName


def getContentType(filename):
    """Returns the content type based on the given filename"""
    return guess_content_type(filename)[0]


@zope.interface.implementer(interfaces.IChunkIterator)
class ChunkIterator(object):
    """Chunk iterator"""

    def __init__(self, reader, chunks):
        self.__id = reader._id
        self.__chunks = chunks
        self.__current_chunk = 0
        self.__max_chunk = math.ceil(float(reader.length) / reader.chunkSize)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current_chunk >= self.__max_chunk:
            raise StopIteration
        chunk = self.__chunks.find_one(
            {"files_id": self.__id, "n": self.__current_chunk})
        if not chunk:
            raise m01.grid.exceptions.CorruptFile(
                "no chunk #%d" % self.__current_chunk)
        self.__current_chunk += 1
        # data = chunk["data"]
        # if isinstance(data, bson.binary.Binary):  # Explicit check for Binary type
        #     return str(data)
        # return data
        return chunk["data"]

    # Python 2 compatibility
    next = __next__


class ChunkLogging(object):
    """Logging support"""

    def _doLog(self, msg, level=logging.DEBUG):
        logger.log(level, '%s %s %s %s' % (self._id, self._chunks.full_name,
            self.__class__.__name__, msg))

    def info(self, msg):
        self._doLog(msg, logging.INFO)

    def debug(self, msg):
        self._doLog(msg, logging.DEBUG)

    def error(self, msg):
        self._doLog(msg, logging.ERROR)


class ChunkHelperMixin(object):
    """Chunk reader and writer helper mixin"""

    def getFilesCollection(self, chunks):
        """Return files collection for given chunk collection"""
        cName = chunks.full_name
        if not cName.endswith('.chunks'):
            raise ValueError("Chunks collection name must end with .chunks")
        fName = '%s.files' % cName[:-7]
        return chunks.database[fName]


@zope.interface.implementer(interfaces.IChunkWriter)
class ChunkWriterBase(ChunkHelperMixin, ChunkLogging):
    """File chunk writer base class

    The mongodb GirdFS specification defines the following key/value:

    {
    "_id" : <unspecified>,      // unique ID for this file
    "length" : data_number,     // size of the file in bytes
    "chunkSize" : data_number,  // size of each of the chunks. (default 256k)
    "uploadDate" : data_date,   // date when object first stored
    "md5" : data_string         // result of running the "filemd5" command
    }

    Another requirement is, that the file and chunk collections must use the
    same prefix and use files and chunks as appendix. This means we need to
    use dotted collection names.

    doc.files
    doc.chunks

    Probably this is for hook up some server side miracles. At least the
    filemd5 database command requires that we use the collection name prefix
    as root name. e.g.

    md5 = database.command("filemd5", self._id, root='doc')["md5"]

    NOTE: we cn only check md5 from admin collection if we store the
    file before the add the chunks. This means we need to commit the
    transaction after adding the file and add the chunk later. This is not
    what we like to do at all. We like to add the chunks before we add the
    file or at least at the same time.

    A ChunkWriterBase based implementation must provide the following
    attributes based on the processing file:

    _id
    _chunks
    _files
    chunkSize
    maxFileSize
    removed

    """

    writeConcern = None
    isUpdate = None

    _filename = None
    _digester = None
    _md5 = None

    def __init__(self, writeConcern=None, skipMD5Check=True, contentType=None,
        encoding=None):
        """Setup ChunkWriterBase basics"""
        self._chunkNumber = 0
        self._buffer = BytesIO()
        self._length = 0
        self._closed = False
        # setup _digester
        self._digester = hashlib.md5()
        self._contentType = contentType
        self._encoding = encoding
        # force write concern
        if writeConcern is None:
            writeConcern = pymongo.write_concern.WriteConcern(j=True)
        self.writeConcern = writeConcern
        self.skipMD5Check = skipMD5Check

    def setUpAcknowledgedWrites(self):
        # ensure aknowledged writes otherwise filemd5 will fail
        if self.writeConcern is None or not self.writeConcern.acknowledged:
            writeConcern = pymongo.write_concern.WriteConcern(j=True)
            self._chunks = self._chunks.with_options(
                write_concern=self.writeConcern)
            self._files = self._chunks.with_options(
                write_concern=self.writeConcern)

    @property
    def closed(self):
        """Return close marker"""
        return self._closed

    def close(self):
        """Flush the file and close it.

        A closed file cannot be written any more. Calling `close` more than
        once is allowed.
        """
        if not self._closed:
            # flush/write last chunks
            self._flushBuffer()
            # apply chunk metadata to adapted FileItem
            self.context.uploadDate = datetime.datetime.now(UTC)
            self.context.md5 = unicode(self._md5)
            self.context.numChunks = self._chunkNumber
            self.context.length = self._length
            self.setFileName(self._filename)
            self.setContentTypeAndEncoding(self._contentType, self._encoding)
            # mark as closed
            self._closed = True
            self.debug('close')

    def validate(self, fileUpload):
        """Validate file upload item"""
        if self._closed:
            raise ValueError("cannot write to a closed file")
        elif not fileUpload or not fileUpload.filename:
            # empty string or None or missing filename means no upload given
            raise ValueError("Missing file upload data")
        elif self.removed:
            raise ValueError("Can't store data for removed files")

    def validateSize(self, data):
        if self.maxFileSize is not None:
            size = self._length + len(data)
            if size > self.maxFileSize:
                raise m01.grid.exceptions.TooLargeFile()

    def makeTMPChunk(self):
        """Move existing chunks away till we uploaded new data"""
        self.debug('make tmp chunk')
        _id = '%s-tmp' % self._id
        self._chunks.update_many({"files_id": self._id},
            {"$set": {'files_id': _id}})

    def revertTMPChunk(self):
        """Revert tmp chunks"""
        self.debug('revert tmp chunk')
        _id = '%s-tmp' % self._id
        self._chunks.update_many({"files_id": _id},
            {"$set": {'files_id': self._id}})

    def removeTMPChunk(self):
        """Remove tmp chunk"""
        self.debug('remove tmp chunk')
        _id = '%s-tmp' % self._id
        self._chunks.delete_many({"files_id": _id})

    def setFileName(self, filename):
        """Set filename (hook for adjust the given filename)"""
        self.context.filename = unicode(filename)

    def getContentTypeAndEncoding(self, filename):
        """Returns the content type based on the given filename"""
        return guess_content_type(filename)

    def setContentTypeAndEncoding(self, contentType, encoding):
        """Set content type (hook for adjust the given type)"""
        if contentType:
            self.context.contentType = unicode(contentType)
        if encoding:
            self.context.encoding = unicode(encoding)

    def doCheckMD5Hash(self):
        """Validate md5

        NOTE: With w=0, 'filemd5' might run before the final chunks are written.
        Make sure you use acknowledged write concern on collection.
        """
        # filemd5 returns the following data
        # {u'md5': u'b10a8db164e0754105b7a99be72e3fe5',
        #  u'ok': 1.0,
        #  u'numChunks': 1}
        if not self.skipMD5Check:
            filemd5 = self._files.database.command("filemd5", self._id,
                root=self._files.full_name)
            numChunks = filemd5['numChunks']
            if self._md5 != filemd5["md5"]:
                # raise exception
                raise ValueError("MD5 hex digest does not match for uploaded data")
            if self._chunkNumber != numChunks:
                raise ValueError("Not correct number of chunks stored")

    # mongo upload helper
    def _flushData(self, data):
        """Flush data to a chunk"""
        if not data:
            return
        assert (len(data) <= self.chunkSize)
        self.validateSize(data)
        self.debug('flush data')

        chunk = {
            "files_id": self._id,
            "n": self._chunkNumber,
            "data": bson.binary.Binary(data),
        }
        self._chunks.insert_one(chunk)
        self._chunkNumber += 1
        self._length += len(data)

    def _flushBuffer(self):
        """Flush the buffer out to a chunk"""
        self._flushData(self._buffer.getvalue())
        self._buffer.close()
        self._buffer = BytesIO()

    def write(self, data):
        """Write data to mongodb"""
        if self._closed:
            raise ValueError("cannot write to a closed file")
        try:
            # file-like
            read = data.read
        except AttributeError:
            data = ensure_utf8_bytes(data)
            read = BytesIO(data).read

        def doRead(chunkSize):
            s = read(self.chunkSize)
            if s:
                self._digester.update(s)
            return s

        if self._buffer.tell() > 0:
            # flush only when _buffer is full
            space = self.chunkSize - self._buffer.tell()
            if space:
                res = doRead(space)
                self._buffer.write(res)
                if len(res) < space:
                    # EOF or incomplete
                    return
            self._flushBuffer()
        # read more
        content = doRead(self.chunkSize)
        while content and len(content) == self.chunkSize:
            self._flushData(content)
            content = doRead(self.chunkSize)
        self._buffer.write(content)

    def add(self, fileUpload):
        """Add file upload as chunk and store metadata"""
        self.validate(fileUpload)
        self._filename = extractFileName(fileUpload.filename)
        self._contentType, self._encoding = self.getContentTypeAndEncoding(
            self._filename)
        # first find out if we have existing chunk data
        self.isUpdate = self._chunks.count_documents({"files_id": self._id})
        if self.isUpdate:
            self.debug('update fileupload')
        else:
            self.debug('add fileupload')
        try:
            if self.isUpdate:
                self.makeTMPChunk()
            # make sure we begin at the start
            fileUpload.seek(0)
            self.write(fileUpload)
            # check md5 hash
            self._md5 = self._digester.hexdigest()
            self.doCheckMD5Hash()
            # close file and force write last chunk
            self.close()
            # cleanup ttmp chunk files
            if self.isUpdate:
                self.removeTMPChunk()
        except Exception as e:
            self.error('add caused an error')
            logger.exception(e)
            # on any exception, we will remove new added chunks
            self._chunks.delete_many({"files_id": self._id})
            # close file without write last chunks
            self._closed = True
            # on update, we revert our TMP chunk
            if self.isUpdate:
                self.revertTMPChunk()
            # and raise the exception
            raise e
        finally:
            self.close()

    def addData(self, data, filename, contentType, encoding=None):
        """Add data as chunk and store metadata"""
        self._filename = filename
        self._contentType = contentType
        if encoding is None:
            encoding = 'utf-8'
        self._encoding = encoding
        # first find out if we have existing chunk data
        self.isUpdate = self._chunks.count_documents({"files_id": self._id})
        if self.isUpdate:
            self.debug('update data')
        else:
            self.debug('add data')
        try:
            # make sure we begin at the start
            self.write(data)
            # check md5 hash
            self._md5 = self._digester.hexdigest()
            self.doCheckMD5Hash()
            # close file and force write last chunk
            self.close()
            # cleanup tmp chunk files
            if self.isUpdate:
                self.removeTMPChunk()
        except Exception as e:
            self.error('addData caused an error')
            logger.exception(e)
            # on any exception, we will remove new added chunks
            self._chunks.delete_many({"files_id": self._id})
            # close file without write last chunks
            self._closed = True
            # on update, we revert our TMP chunk
            if self.isUpdate:
                self.revertTMPChunk()
            # and raise the exception
            raise e

    def remove(self):
        """Mark chunk data as removed"""
        self._chunks.update_many({"files_id": self._id},
            {"$set": {'removed': True}})

    def __enter__(self):
        """Support for the context manager protocol"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for the context manager protocol.

        Close the file and allow exceptions to propogate.
        """
        self.close()
        # propogate exceptions
        return False


class ChunkWriter(ChunkWriterBase):
    """File chunk writer adapter"""

    zope.component.adapts(interfaces.IFile)

    def __init__(self, context, writeConcern=None):
        """Setup ChunkWriter based on adapted context"""
        super(ChunkWriter, self).__init__(writeConcern=writeConcern)
        self.context = context
        self._id = context._id
        if not self._id:
            raise ValueError("Missing mongo ObjectId", self._id)
        # setup collections
        if not self.context.chunkCollection.full_name.endswith('.chunks'):
            raise ValueError("Chunks collection name must end with .chunks")
        self._chunks = self.context.chunkCollection
        self._files = self.getFilesCollection(self._chunks)
        if not self._files.write_concern.acknowledged:
            raise pymongo.errors.ConfigurationError(
                u"Files collection must use acknowledged write_concern. "
                u"Otherwise filemd5 might run before the final chunks are "
                u"written")
        self.chunkSize = self.context.chunkSize
        self.maxFileSize = self.context.maxFileSize
        self.removed = self.context.removed
        # ensure aknowledged writes
        self.setUpAcknowledgedWrites()


@zope.interface.implementer(interfaces.IChunkReader)
class ChunkReaderBase(ChunkHelperMixin, ChunkLogging):
    """File chunk reader adapter

    A ChunkReaderBase absed implementation must provide the following
    attributes:

    _id          file _id
    _chunks      (chunk collection, must end with ``.chunks``)
    _files       (chunk collection, must end with ``.files``)
    chunkSize    chunk size
    numChunks    number of chunks
    length       file size
    contentType  content type
    removed      marker for removed files

    """


    def __init__(self):
        self._buffer = b""
        self._position = 0

    @property
    def size(self):
        """simply map length as size (common in zope)"""
        return self.length

    @property
    def __name__(self):
        """simply map filename as __name__ (common in zope)"""
        return self.filename

    def validate(self):
        if self.removed:
            raise ValueError("Can't read data from removed files")

    def read(self, size=-1):
        """Read at most `size` bytes from the file

        If size is negative or omitted all data is read
        Returns bytes in both Python 2 and 3
        """
        # validate read operation
        self.validate()

        if size == 0:
            return b""

        remainder = int(self.length) - self._position
        if size < 0 or size > remainder:
            size = remainder

        received = len(self._buffer)
        chunkNumber = old_div((received + self._position), self.chunkSize)
        chunks = []

        while received < size:
            chunk = self._chunks.find_one({"files_id": self._id, "n": chunkNumber})
            if not chunk:
                raise m01.grid.exceptions.CorruptFile("no chunk #%d" % chunkNumber)

            chunk_data = chunk["data"]
            if not received:
                # first chunk
                chunk_data = chunk_data[self._position % self.chunkSize:]

            received += len(chunk_data)
            chunks.append(chunk_data)
            chunkNumber += 1

        if self.numChunks != chunkNumber:
            raise m01.grid.exceptions.CorruptFile(
                "Used chunk number '%s' does not fit" % chunkNumber,
                self.numChunks)

        data = b"".join([self._buffer] + chunks)
        self._position += size
        to_return = data[:size]
        self._buffer = data[size:]
        return to_return

    def readline(self, size=-1):
        """Read one line or up to `size` bytes from the file"""
        res = ""
        while len(res) != size:
            byte = self.read(1)
            res += byte
            if byte == "" or byte == "\n":
                break
        return res

    def tell(self):
        """Return the current position of this file"""
        return self._position

    def seek(self, pos, whence=_SEEK_SET):
        """Set the current position of this file"""
        if whence == _SEEK_SET:
            new_pos = pos
        elif whence == _SEEK_CUR:
            new_pos = self._position + pos
        elif whence == _SEEK_END:
            new_pos = int(self.length) + pos
        else:
            raise IOError(22, "Invalid value for `whence`")
        if new_pos < 0:
            raise IOError(22, "Invalid value for `pos` - must be positive")
        self._position = new_pos
        self._buffer = b""

    def __iter__(self):
        """Return an iterator over all of this file's data"""
        # validate read operation
        self.validate()
        # return iterator
        return ChunkIterator(self, self._chunks)

    def close(self):
        """Support file-like API"""
        pass

    def __enter__(self):
        """Makes it possible to use with the context manager protocol"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Makes it possible to use with the context manager protocol"""
        return False


class ChunkReader(ChunkReaderBase):
    """File chunk reader adapter

    The context adapting ChunkReader uses the chunkCollectioin attribute
    from the adapting item for setup the files collection"""

    zope.component.adapts(interfaces.IFile)

    def __init__(self, context):
        """Setup chunk reader based on adapted context"""
        super(ChunkReader, self).__init__()
        self.context = context
        self._id = context._id
        if not self._id:
            raise ValueError("Missing mongo ObjectId", self._id)
        self._chunks = self.context.chunkCollection
        if not self._chunks.full_name.endswith('.chunks'):
            raise ValueError("Chunks collection name must end with .chunks")
        self._files = self.getFilesCollection(self._chunks)
        if not self._files.full_name.endswith('.files'):
            raise ValueError("Files collection name must end with .files")

        # IGridFSSpecification
        self.length = self.context.length
        self.chunkSize = self.context.chunkSize
        self.uploadDate = self.context.uploadDate
        self.md5 = self.context.md5
        self.filename = self.context.filename
        self.contentType = self.context.contentType
        # IFile
        self.numChunks = self.context.numChunks
        self.removed = self.context.removed


class ChunkDataReader(ChunkReaderBase):
    """Chunk data reader based on given mongodb file data

    NOTE: the ChunkDataReader uses the files collceiton and not the chunks
    collection as __init__ argument. The data argument must provide the file
    data as dict.
    """

    def __init__(self, filesCollection, data):
        """Setup chunk reader based on given file data"""
        super(ChunkDataReader, self).__init__()
        self._id = data['_id']
        if not self._id:
            raise ValueError("Missing mongo ObjectId", self._id)
        # setup files collection
        self._files = filesCollection
        if not self._files.full_name.endswith('.files'):
            raise ValueError("Fiels collection name must end with .files")
        # setup chunks collection
        chunksName = '%s.chunks' % self._files.full_name[:-6]
        self._chunks = self._files.database[chunksName]
        if not self._chunks.full_name.endswith('.chunks'):
            raise ValueError("Chunks collection name must end with .chunks")

        # IGridFSSpecification
        self.length = data['length']
        self.chunkSize = data['chunkSize']
        self.uploadDate = data['uploadDate']
        self.md5 = data['md5']
        self.filename = data['filename']
        self.contentType = data['contentType']
        # IFile
        self.numChunks = data['numChunks']
        self.removed = data['removed']


def getChunkDataReader(collection, query):
    """Lookup a file and return a ChunkDataReader"""
    # get data
    data = collection.find_one(query)
    return ChunkDataReader(collection, data)


def getChunkDataReaders(collection, query):
    """Lookup one or more file and return the chunk readers

    This is usefull for get files and process them later e.g. collect
    email attachements for processing. But take care, there is no filename or
    other file meta data such chunks. Only use a such chunk reader if you know
    what you are doing ;-). Probably a better idea is to use a ChunkReader.
    """
    # get data
    for data in collection.find(query):
        yield ChunkDataReader(collection, data)
