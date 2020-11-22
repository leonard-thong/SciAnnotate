# -*- coding:utf-8 -*-
"""
===========================================
  @author:  leonard, Robin 
  @time:    2020/10/29 4:52 PM
  @project: brat
  @file:    newDocument.py
===========================================
"""

import os
from document import real_directory
from os.path import join as path_join
from utils import GLOBAL_LOGGER

def create_new_document(**kwargs):
    res = dict()
    collection = kwargs['collection']
    document = kwargs['document']
    text = kwargs['text']
    # check if the file has been uploaded 
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    f = open(document + '.txt', 'w')
    f.write(text)
    return res

def import_new_document(**kwargs):
    res = dict()
    collection = kwargs['collection']
    document = kwargs['document']
    GLOBAL_LOGGER.log_normal(document)
    text = kwargs['text']
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    f = open(document + '.txt', 'w')
    f.write(text)
    return res