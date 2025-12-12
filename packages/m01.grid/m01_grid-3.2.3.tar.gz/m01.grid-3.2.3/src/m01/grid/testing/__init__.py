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
__docformat__ = "reStructuredText"

from builtins import object

import os
import sys
import tempfile

import pymongo
import six

import zope.schema
import zope.interface
from zope.publisher.browser import FileUpload
from zope.testing.loggingsupport import InstalledHandler

import m01.mongo.interfaces
import m01.mongo.testing
import m01.stub.testing
import m01.grid.item
from m01.mongo.fieldproperty import MongoFieldProperty
from m01.grid import interfaces

# mongo db name used for testing
TEST_DB_NAME = 'm01_grid_testing'
TEST_COLLECTION_NAME = 'test'
TEST_COLLECTION_FULL_NAME = '%s.%s' % (TEST_DB_NAME,
    TEST_COLLECTION_NAME)
TEST_FILES_COLLECTION_NAME = '%s.files' % TEST_COLLECTION_NAME
TEST_FILES_COLLECTION_FULL_NAME = '%s.%s.%s' % (TEST_DB_NAME,
    TEST_COLLECTION_NAME, TEST_FILES_COLLECTION_NAME)
TEST_CHUNKS_COLLECTION_NAME = '%s.chunks' % TEST_COLLECTION_NAME
TEST_CHUNKS_COLLECTION_FULL_NAME = '%s.%s.%s' % (TEST_DB_NAME,
    TEST_COLLECTION_NAME, TEST_CHUNKS_COLLECTION_NAME)


##############################################################################
#
# test setup methods
#
##############################################################################

_testClient = None

def getTestClient():
    return _testClient

def getTestDatabase():
    client = getTestClient()
    return client[TEST_DB_NAME]

def getTestCollection():
    db = getTestDatabase()
    return db[TEST_COLLECTION_NAME]

def getTestFilesCollection():
    db = getTestDatabase()
    return db[TEST_FILES_COLLECTION_NAME]

def getTestChunksCollection():
    db = getTestDatabase()
    return db[TEST_CHUNKS_COLLECTION_NAME]

def dropTestDatabase():
    client = getTestClient()
    client.drop_database(TEST_DB_NAME)

def dropTestFilesCollection():
    db = getTestDatabase()
    db.drop_collection(TEST_CHUNKS_COLLECTION_NAME)

def dropTestChunkCollection():
    db = getTestDatabase()
    db.drop_collection(TEST_CHUNKS_COLLECTION_NAME)


# stub mongodb server
def setUpStubMongo(test=None):
    """Setup pymongo client as test client and setup a real empty mongodb"""
    host = 'localhost'
    port = 45017
    tz_aware = True
    sandBoxDir = os.path.join(os.path.dirname(__file__), 'sandbox')
    options = [
        # smaller file size for faster start/stop
        # '--nojournal', journal is required for write concern and filemd5
        '--smallfiles', '--nssize', '10',
        # add dbpath
        '--dbpath']
    m01.stub.testing.startMongoServer(host, port, options,
        sandBoxDir=sandBoxDir)
    # setup pymongo.MongoClient as test client
    global _testClient
    # force aknowledged writes
    _testClient = pymongo.MongoClient(host, port, tz_aware=tz_aware,
        journal=True)
    logger = InstalledHandler('m01.grid')
    test.globs['logger'] = logger


def tearDownStubMongo(test=None):
    """Tear down real mongodb"""
    # stop mongodb server
    sleep = 0.5
    m01.stub.testing.stopMongoServer(sleep)
    # reset test client
    global _testClient
    _testClient = None
    logger = test.globs['logger']
    logger.clear()
    logger.uninstall()
    # clear thread local transaction cache
    m01.mongo.clearThreadLocalCache()


###############################################################################
#
# test helper
#
###############################################################################

class FakeFieldStorage(object):
    """A fake field storage"""

    def __init__(self, upload, filename, headers):
        self.file = upload
        self.filename = filename
        self.headers = headers

def getFileUpload(txt, filename=None, headers=None):
    if filename is None:
        filename = 'test.txt'
    if headers is None:
        headers = {}
    if sys.version_info[0] >= 3:
        if isinstance(txt, str):
            txt = txt.encode('utf-8')
    else:
        if isinstance(txt, unicode):
            txt = txt.encode('utf-8')

    upload = tempfile.SpooledTemporaryFile(mode='w+b')
    upload.write(txt)
    upload.seek(0)
    fieldStorage = FakeFieldStorage(upload, filename, headers)
    return FileUpload(fieldStorage)


###############################################################################
#
# Public Base Tests
#
###############################################################################

class FileItemBaseTest(m01.mongo.testing.MongoItemBaseTest):
    """fileItem base test"""

    def test_providedBy_IFile(self):
        obj = self.makeTestObject()
        self.assert_(interfaces.IFile.providedBy(obj), True)

    def test_providedBy_IFileItem(self):
        obj = self.makeTestObject()
        self.assert_(interfaces.IFileItem.providedBy(obj), True)


class FileObjectBaseTest(m01.mongo.testing.MongoObjectBaseTest):
    """fileItem base test"""

    def test_providedBy_IFile(self):
        obj = self.makeTestObject()
        self.assert_(interfaces.IFile.providedBy(obj), True)

    def test_providedBy_IFileObject(self):
        obj = self.makeTestObject()
        self.assert_(interfaces.IFileObject.providedBy(obj), True)


###############################################################################
#
# test components
#
###############################################################################

class TestFilesCollectionMixin(object):
    """Test files collection mixin class"""

    @property
    def collection(self):
        return getTestFilesCollection()

class TestChunksCollectionMixin(object):
    """Test chunks collection mixin class"""

    @property
    def chunkCollection(self):
        return getTestChunksCollection()


class ITestSchema(zope.interface.Interface):
    """Basic test schema."""

    title = zope.schema.TextLine(
        title=u'Title',
        description=u'Title',
        default=u'',
        required=True)

    description = zope.schema.Text(
        title=u'Description',
        description=u'Description',
        default=u'',
        required=False)


class ISampleFileStorageItem(ITestSchema, interfaces.IFileStorageItem):
    """Sample storage file item interface."""

    __name__ = zope.schema.TextLine(
        title=u'Title',
        description=u'Title',
        missing_value=u'',
        default=None,
        required=True)


@zope.interface.implementer(ISampleFileStorageItem)
class SampleFileStorageItem(TestChunksCollectionMixin,
    m01.grid.item.FileStorageItem):
    """Sample file storage item."""


    title = MongoFieldProperty(ISampleFileStorageItem['title'])
    description = MongoFieldProperty(ISampleFileStorageItem['description'])

    dumpNames = ['title', 'description']


class ISampleFileStorage(m01.mongo.interfaces.IMongoStorage):
    """Sample file storage interface."""


@zope.interface.implementer(ISampleFileStorage)
class SampleFileStorage(TestFilesCollectionMixin,
    m01.mongo.storage.MongoStorage):
    """Sample file storage."""


    def __init__(self):
        pass

    def load(self, data):
        """Load data into the right mongo item."""
        return SampleFileStorageItem(data)