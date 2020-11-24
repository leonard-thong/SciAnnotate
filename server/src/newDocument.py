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
    res['action'] = kwargs['action']
    #GLOBAL_LOGGER.log_normal( kwargs)
    try:
      collection = kwargs['collection']
      directory = collection
      real_dir = real_directory(directory)
      for i in range(0, 1000):
        fileName = kwargs.get('files[{}][name]'.format(i))
        fileContent = kwargs.get('files[{}][content]'.format(i))
        if not fileName or not fileContent: break
        document = path_join(real_dir, fileName)
        if document[-3:] == 'txt':
          f = open(document, 'w')
        else:
          document = document[:-len(document.split('.')[-1]) - 1] + '.txt'
        with open(document, 'w') as f:
          f.write(fileContent)
          f.close()
      res['status'] = 200
    except Exception as e:
      res['status'] = 503
    return res
