# make a package

from __future__ import absolute_import
import bson.son

import pymongo
import pymongo.errors


FILE_INDEX = bson.son.SON([
    ("filename", pymongo.ASCENDING),
    ("uploadDate", pymongo.ASCENDING)
    ])

CHUNK_INDEX = bson.son.SON([
    ("files_id", pymongo.ASCENDING),
    ("n", pymongo.ASCENDING)
    ])


def setUpIndex(collection, idx, unique, session=None):
    doc = collection.find_one(projection={"_id": 1}, session=session)
    if doc is None:
        try:
            keys = [spec['key'] for spec in
                    collection.list_indexes(session=session)]
        except pymongo.errors.OperationFailure:
            keys = []
        if idx not in keys:
            collection.create_index(list(idx.items()), unique=unique, session=session)


def setUpGridFSIndex(collection):
    """Setup grid collection indexes"""
    setUpIndex(collection.files, FILE_INDEX, False)
    setUpIndex(collection.chunks, CHUNK_INDEX, True)