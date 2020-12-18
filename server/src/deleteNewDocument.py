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
    if os.path.isdir(document):
        os.remove(document)
    else:
        os.remove(document+'.txt')
        os.remove(document+'.ann')
        if os.path.exists(document+'_func.ann'):
            os.remove(document+'_func.ann')
    return res
