# -*- coding:utf-8 -*-
"""
===========================================
  @author:  leonard, Robin 
  @time:    2020/10/29 4:52 PM
  @project: brat
  @file:    createNewDocument.py
===========================================
"""

import os
from utils import GLOBAL_LOGGER
from document import real_directory
from os.path import join as path_join

def create_new_document(**kwargs):
    res = dict()
    collection = kwargs['collection']

    document = kwargs['document']
    text = kwargs['text']
    # check if the file has been uploaded 
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    f = open(document, 'w')
    f.write(text)
    return res