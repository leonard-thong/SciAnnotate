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

def create_new_document(**kwargs):
    res = dict()
    collection = kwargs['collection']

    document = kwargs['document']
    text = kwargs['text']
    # check if the file has been uploaded 
    path = collection + '/' + document
    GLOBAL_LOGGER.log_normal(collection)
    open(path, 'wb').write(text) 
    return res