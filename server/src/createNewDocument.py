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


def create_new_document(**kwargs):
    res = dict()
    collection = kwargs['collection']
    document = kwargs['document']
    text = kwargs['text']
    # check if the file has been uploaded 
    if fileitem.filename: 
        # strip the leading path from the file name 
        fn = os.path.basename(fileitem.filename) 
        # open read and write the file into the server 
        path = collection + '/' + document
        open(path, 'wb').write(text) 
    return res