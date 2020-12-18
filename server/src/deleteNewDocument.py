import os
from document import real_directory
from os.path import join as path_join
from utils import GLOBAL_LOGGER

def delete_new_document(**kwargs):
    GLOBAL_LOGGER.log_normal(kwargs.__str__())
    res = dict()
    collection = kwargs['collection']
    document = kwargs['document']
    directory = collection
    real_dir = real_directory(directory)
    GLOBAL_LOGGER.log_normal(real_dir)
    document = path_join(real_dir, document)
    os.remove(document)
    return res
