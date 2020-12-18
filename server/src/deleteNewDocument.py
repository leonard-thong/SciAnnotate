import os
from document import real_directory
from os.path import join as path_join

def delete_new_document(**kwargs):
    res = dict()
    collection = kwargs['collection']
    document = kwargs['document']
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    os.remove(document)
    return res
