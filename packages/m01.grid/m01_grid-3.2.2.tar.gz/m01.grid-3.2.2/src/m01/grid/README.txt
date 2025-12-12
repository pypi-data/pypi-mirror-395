======
README
======

This package provides a grid file and storage implementation for zope3. This
means we offer a file and storage which is able to handle file upload and store
the file content in a mongodb database.

NOTE
----

This implementation is not compatible with the default gridfs implementation
from mongodb. Our implementation uses a custom collection for store an item
including the meta data and only stores the additional chunks in a chunk
collection.


How we process file upload
--------------------------

This description defines how a file upload will get processd in some raw
steps. It defines some internal part we use for processing an input stream
but it doesn't really explain how we implemented the grid file pattern.

The browser defins a form with a file upload input field:

  - client starts file upload

The file upload will get sent to the server:

  - create request

  - read input stream

  - process input stream

    - define cgi parser (p01.cgi.parser.parseFormData)

    - parse input stream with cgi parser

      - write file upload part in tmp file

      - wrap file upload part from input stream with FileUpload

    - store FileUpload instance in request.form with the form input field
      name as key

The file upload get processed from the request by using z3c.form components:

  - z3c.form defines a widget

  - z3c.widget reads the FileUpload from the request

  - z3c.form data converter returns the plain FileUpload

  - z3c.form data manager stores the FileUpload as attribute value

Each file item provides an fileUpload property (attribute) which is responsible
to process the given FileUpload object. The defualt built-in fileUpload
property does the following:

  - get a FileWriter

The FileWrite knows how to write the given FileUpload tmp file to mongodb.


setup
-----

  >>> import re
  >>> import sys
  >>> import hashlib
  >>> from pprint import pprint
  >>> from pymongo import ASCENDING
  >>> import transaction
  >>> import m01.mongo.testing
  >>> import m01.grid.testing

Also define a normalizer:

  >>> patterns = [
  ...    (re.compile(r"ObjectId\('[a-zA-Z0-9]+'\)"), r"ObjectId('...')"),
  ...    (re.compile(r"datetime.datetime\([a-zA-Z0-9, ]+tzinfo=<bson.tz_util.FixedOffset[a-zA-Z0-9 ]+>\)"), "datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>)"),
  ...    (re.compile(r"datetime.datetime\([a-zA-Z0-9, ]+tzinfo=[a-zA-Z0-9>]+\)"), "datetime(..., tzinfo= ...)"),
  ...    (re.compile(r"datetime\([a-z0-9, ]+\)"), "datetime(...)"),
  ...    (re.compile(r"object at 0x[a-zA-Z0-9]+"), "object at "),
  ...    (re.compile(r"u'__name__':"), r"'__name__':"),
  ...    (re.compile(r"'__name__': '[a-zA-Z0-9]+'"), r"'__name__': '...'"),
  ...    (re.compile(r"u'_id':"), r"'_id':"),
  ...    (re.compile(r"u'_type':"), r"'_type':"),
  ...    (re.compile(r"u'_pid':"), r"'_pid':"),
  ...    (re.compile(r"u'_version':"), r"'_version':"),
  ...    (re.compile(r"u'chunkSize':"), r"'chunkSize':"),
  ...    (re.compile(r"u'created':"), r"'created':"),
  ...    (re.compile(r"u'description':"), r"'description':"),
  ...    (re.compile(r"u'title':"), r"'title':"),
  ...    (re.compile(r"u'filename':"), r"'filename':"),
  ...    (re.compile(r"u'md5':"), r"'md5':"),
  ...    (re.compile(r"u'length':"), r"'length':"),
  ...    (re.compile(r"u'modified':"), r"'modified':"),
  ...    (re.compile(r"u'numChunks':"), r"'numChunks':"),
  ...    (re.compile(r"u'removed':"), r"'removed':"),
  ...    (re.compile(r"u'uploadDate':"), r"'uploadDate':"),
  ...    (re.compile(r"u'contentType':"), r"'contentType':"),
  ...    (re.compile(r"u'encoding':"), r"'encoding':"),
  ...    (re.compile(r"u'key':"), r"'key':"),
  ...    (re.compile(r"u'name':"), r"'name':"),
  ...    (re.compile(r"u'ns':"), r"'ns':"),
  ...    (re.compile(r"u'v':"), r"'v':"),
  ...    (re.compile(r"u'unique':"), r"'unique':"),
  ...    (re.compile(r"u'files_id':"), r"'files_id':"),
  ...    (re.compile(r"u'data':"), r"'data':"),
  ...    (re.compile(r"u'n':"), r"'n':"),
  ...    (re.compile(r"u'filename':"), r"'filename':"),
  ...    (re.compile(r"u'uploadDate':"), r"'uploadDate':"),
  ...    (re.compile(r"u'm01_grid_testing'"), r"'m01_grid_testing'"),
  ...    (re.compile(r"u'test.chunks'"), r"'test.chunks'"),
  ...    (re.compile(r"'key': u'"), r"'key': '"),
  ...    (re.compile(r"'name': u'"), r"'name': '"),
  ...    (re.compile(r"'_id': u'"), r"'_id': '"),
  ...    (re.compile(r"'ns': u'"), r"'ns': '"),
  ...    (re.compile(r"'v': u'"), r"'v': '"),
  ...    (re.compile(r"'md5': u'"), r"'md5': '"),
  ...    (re.compile(r"'_type': u'"), r"'_type': '"),
  ...    (re.compile(r"'contentType': u'"), r"'contentType': '"),
  ...    (re.compile(r"'title': u'"), r"'title': '"),
  ...    (re.compile(r"'description': u'"), r"'description': '"),
  ...    (re.compile(r"'unique': u'"), r"'unique': '"),
  ...    (re.compile(r"'filename': u'"), r"'filename': '"),
  ...    (re.compile(r"Binary\('"), r"Binary(b'"),
  ...    (re.compile(r"'data': Binary\(b'(.*?)', 0\),"), r"'data': b'\1',")
  ...    ]

  >>> reNormalizer = m01.mongo.testing.RENormalizer(patterns)

Convert chunk to simple output used for python 2/3:

  >>> def print_bytes(chunk):
  ...     if isinstance(chunk, bytes):
  ...         chunk = chunk.decode('utf-8')
  ...     print(chunk)

Test the grid storage:

  >>> db = m01.grid.testing.getTestDatabase()

  >>> chunks = m01.grid.testing.getTestChunksCollection()
  >>> print(chunks.full_name)
  m01_grid_testing.test.chunks

  >>> files = m01.grid.testing.getTestFilesCollection()
  >>> print(files.full_name)
  m01_grid_testing.test.files

  >>> storage = m01.grid.testing.SampleFileStorage()
  >>> storage
  <m01.grid.testing.SampleFileStorage object at ...>

Our test setup offers a log handler where we can use like:

  >>> logger.clear()
  >>> print(logger)

Let's first setup the gridfs indexes:

  >>> collection = m01.grid.testing.getTestCollection()

  >>> for spec in collection.files.list_indexes():
  ...     reNormalizer.pprint(spec)

  >>> for spec in collection.chunks.list_indexes():
  ...     reNormalizer.pprint(spec)

  >>> m01.grid.setUpGridFSIndex(collection)
  >>> for spec in collection.files.list_indexes():
  ...     reNormalizer.pprint(spec)
  {'key': {'_id': 1},
   'name': '_id_',
   'ns': 'm01_grid_testing.test.files',
   'v': 2}
  {'key': {'filename': 1, 'uploadDate': 1},
   'name': 'filename_1_uploadDate_1',
   'ns': 'm01_grid_testing.test.files',
   'v': 2}

  >>> m01.grid.setUpGridFSIndex(collection)
  >>> for spec in collection.chunks.list_indexes():
  ...     reNormalizer.pprint(spec)
  {'key': {'_id': 1},
   'name': '_id_',
   'ns': 'm01_grid_testing.test.chunks',
   'v': 2}
  {'key': {'files_id': 1, 'n': 1},
   'name': 'files_id_1_n_1',
   'ns': 'm01_grid_testing.test.chunks',
   'unique': True,
   'v': 2}


FileStorageItem
---------------

The FileStorageItem is implemented as a IMongoStorageItem and provides IFile.
This item can get stored in a IMongoStorage. This is known as the
container/item pattern. This contrainer only defines an add method which
implicit uses the items __name__ as key.

  >>> txt = 'Hello World äöü'
  >>> text = txt
  >>> if sys.version_info[0] >= 3:
  ...     text = txt.encode('utf-8')
  >>> digester = hashlib.md5()
  >>> digester.update(text)
  >>> md5 = digester.hexdigest()
  >>> md5
  '6d92a019ac8841573340aeaa06713032'

  >>> length = len(text)
  >>> length
  18

  >>> upload = m01.grid.testing.getFileUpload(txt)
  >>> upload.filename == 'test.txt'
  True

  >>> upload.headers
  {}

  >>> print(upload.read().decode('utf-8'))
  Hello World äöü

  >>> ignored = upload.seek(0)

  >>> data = {'title': u'title', 'description': u'description'}
  >>> item = m01.grid.testing.SampleFileStorageItem(data)
  >>> firstID = item._id

  >>> reNormalizer.pprint(item.chunkCollection)
  Collection(Database(MongoClient(host=['localhost:45017'], document_class=dict, tz_aware=True, connect=True, journal=True), 'm01_grid_testing'), 'test.chunks')

And apply the file upload item:

  >>> item.applyFileUpload(upload)

Let's validate the data:

  >>> print(item.md5)
  6d92a019ac8841573340aeaa06713032

  >>> item.md5 == md5
  True

  >>> item.length
  18

  >>> item.length == length
  True

And we've got a log entry:

  >>> print(logger)
  m01.grid DEBUG
    ... m01_grid_testing.test.chunks ChunkWriter add fileupload
  m01.grid DEBUG
    ... m01_grid_testing.test.chunks ChunkWriter flush data
  m01.grid DEBUG
    ... m01_grid_testing.test.chunks ChunkWriter close

  >>> logger.clear()

Now let's see how our FileItem get enhanced with the chunk info:

  >>> reNormalizer.pprint(item.__dict__)
  {'_id': ObjectId('...'),
  '_m_changed': True,
  '_m_initialized': True,
  '_m_parent': None,
  '_pid': None,
  '_type': 'SampleFileStorageItem',
  '_version': 0,
  'contentType': 'text/plain',
  'created': datetime(..., tzinfo= ...),
  'description': 'description',
  'filename': 'test.txt',
  'length': 18,
  'md5': '6d92a019ac8841573340aeaa06713032',
  'numChunks': 1,
  'title': 'title',
  'uploadDate': datetime(..., tzinfo= ...)}

  >>> reNormalizer.pprint(item.dump())
  {'__name__': '...',
   '_id': ObjectId('...'),
   '_pid': None,
   '_type': 'SampleFileStorageItem',
   '_version': 0,
   'chunkSize': 261120,
   'contentType': 'text/plain',
   'created': datetime(..., tzinfo= ...),
   'description': 'description',
   'encoding': None,
   'filename': 'test.txt',
   'length': 18,
   'md5': '6d92a019ac8841573340aeaa06713032',
   'modified': None,
   'numChunks': 1,
   'removed': False,
   'title': 'title',
   'uploadDate': datetime(..., tzinfo= ...)}

As you can see we can lookup the chunks from our chunks collection by calling
find_one. Note, we should not use find and iterate, then this whould let a
cursor open and more important not use our chunk index which requires using
`files_id` and `n` fields:

  >>> reNormalizer.pprint(chunks.find_one({'files_id': item._id, 'n': 0}))
  {'_id': ObjectId('...'),
   'data': b'Hello World \xc3\xa4\xc3\xb6\xc3\xbc',
   'files_id': ObjectId('...'),
   'n': 0}

Now let's store our item in our storage:

  >>> key = storage.add(item)
  >>> len(key)
  24

  >>> reNormalizer.pprint(item.__dict__)
  {'_id': ObjectId('...'),
   '_m_changed': True,
   '_m_initialized': True,
   '_m_parent': <m01.grid.testing.SampleFileStorage object at >,
   '_pid': None,
   '_type': 'SampleFileStorageItem',
   '_version': 0,
   'contentType': 'text/plain',
   'created': datetime(..., tzinfo= ...),
   'description': 'description',
   'filename': 'test.txt',
   'length': 18,
   'md5': '6d92a019ac8841573340aeaa06713032',
   'numChunks': 1,
   'title': 'title',
   'uploadDate': datetime(..., tzinfo= ...)}


  >>> reNormalizer.pprint(item.dump())
  {'__name__': '...',
   '_id': ObjectId('...'),
   '_pid': None,
   '_type': 'SampleFileStorageItem',
   '_version': 0,
   'chunkSize': 261120,
   'contentType': 'text/plain',
   'created': datetime(..., tzinfo= ...),
   'description': 'description',
   'encoding': None,
   'filename': 'test.txt',
   'length': 18,
   'md5': '6d92a019ac8841573340aeaa06713032',
   'modified': None,
   'numChunks': 1,
   'removed': False,
   'title': 'title',
   'uploadDate': datetime(..., tzinfo= ...)}


Now let's commit the items to mongo:

  >>> transaction.commit()

Now let's read the file data:

  >>> item = storage.get(key)
  >>> reader = item.getFileReader()

  >>> print(reader.read().decode('utf-8'))
  Hello World äöü

  >>> reader.seek(0)

  >>> for chunk in reader:
  ...     print_bytes(chunk)
  Hello World äöü


compatibilty
------------

Our implementation is compatible with the gridfs implementation. But take care
if you write file objects to the mongodb with the gridfs library and don't
forget to add the required data the application uses for the specific FileItem.

First let's see what we have stored in ou files collection:

  >>> files = m01.grid.testing.getTestFilesCollection()
  >>> for data in files.find():
  ...     reNormalizer.pprint(data)
  {'__name__': ...,
   '_id': ObjectId('...'),
   '_pid': None,
   '_type': 'SampleFileStorageItem',
   '_version': 1,
   'chunkSize': 261120,
   'contentType': 'text/plain',
   'created': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>),
   'description': 'description',
   'encoding': None,
   'filename': 'test.txt',
   'length': 18,
   'md5': '6d92a019ac8841573340aeaa06713032',
   'modified': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>),
   'numChunks': 1,
   'removed': False,
   'title': 'title',
   'uploadDate': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>)}

Now let's test how we can read with gridfs:

  >>> import gridfs
  >>> grid = gridfs.GridFS(db, 'test')
  >>> f = grid.get(firstID)
  >>> f
  <gridfs.grid_file.GridOut object at ...>

  >>> print(f.read().decode('utf-8'))
  Hello World äöü

Test iterator:

  >>> reader.seek(0)

  >>> for chunk in f:
  ...     print_bytes(chunk)
  Hello World äöü


update
------

We can also update a file by apply a new fileUpload:

  >>> txt = 'Hello NEW World äöü'
  >>> newUpload = m01.grid.testing.getFileUpload(txt)
  >>> newUpload.filename = 'new.txt'
  >>> newUpload.filename
  'new.txt'

  >>> item = storage.get(key)
  >>> item.applyFileUpload(newUpload)

As you can see our logger reports that the previous chunk get marked as tmp and
after upload removed:

  >>> print(logger)
  m01.grid DEBUG
    ... m01_grid_testing.test.chunks ChunkWriter update fileupload
  m01.grid DEBUG
    ... m01_grid_testing.test.chunks ChunkWriter make tmp chunk
  m01.grid DEBUG
    ... m01_grid_testing.test.chunks ChunkWriter flush data
  m01.grid DEBUG
    ... m01_grid_testing.test.chunks ChunkWriter close
  m01.grid DEBUG
    ... m01_grid_testing.test.chunks ChunkWriter remove tmp chunk

  >>> logger.clear()

before we commit, let's check if we get a _m_changed marker:

  >>> reNormalizer.pprint(item.__dict__)
  {'_id': ObjectId('...'),
   '_m_changed': True,
   '_m_initialized': True,
   '_m_parent': <m01.grid.testing.SampleFileStorage object at >,
   '_pid': None,
   '_type': 'SampleFileStorageItem',
   '_version': 1,
   'contentType': 'text/plain',
   'created': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>),
   'description': 'description',
   'filename': 'new.txt',
   'length': 22,
   'md5': '1d411e2de86c5207d2bcc9efe214957f',
   'modified': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>),
   'numChunks': 1,
   'title': 'title',
   'uploadDate': datetime(..., tzinfo= ...)}


commit transaction and check the item:

  >>> transaction.commit()

Now let's check if the storage cache ist empty and we don't get the
cached item without the changed data:

  >>> storage._cache
  {}

Check what we have in mongo:

  >>> files = m01.grid.testing.getTestFilesCollection()
  >>> for data in files.find():
  ...     reNormalizer.pprint(data)
  {'__name__': ...,
   '_id': ObjectId('...'),
   '_pid': None,
   '_type': 'SampleFileStorageItem',
   '_version': 2,
   'chunkSize': 261120,
   'contentType': 'text/plain',
   'created': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>),
   'description': 'description',
   'encoding': None,
   'filename': 'new.txt',
   'length': 22,
   'md5': '1d411e2de86c5207d2bcc9efe214957f',
   'modified': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>),
   'numChunks': 1,
   'removed': False,
   'title': 'title',
   'uploadDate': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>)}

And let's load the item with our storage:

  >>> item = storage.get(key)
  >>> reNormalizer.pprint(item.__dict__)
  {'_id': ObjectId('...'),
   '_m_changed': False,
   '_m_initialized': True,
   '_m_parent': <m01.grid.testing.SampleFileStorage object at >,
   '_pid': None,
   '_type': 'SampleFileStorageItem',
   '_version': 2,
   'contentType': 'text/plain',
   'created': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>),
   'description': 'description',
   'filename': 'new.txt',
   'length': 22,
   'md5': '1d411e2de86c5207d2bcc9efe214957f',
   'modified': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>),
   'numChunks': 1,
   'title': 'title',
   'uploadDate': datetime(..., tzinfo=<bson.tz_util.FixedOffset ...>)}

Now let's read the file data:

  >>> reader = item.getFileReader()
  >>> print_bytes(reader.read())
  Hello NEW World äöü

  >>> for chunk in reader:
  ...     print_bytes(chunk)
  Hello NEW World äöü


FileObject
----------

The FileObject provides IFile and IMongoObject.