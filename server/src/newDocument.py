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
import shutil
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

def create_folder(**kwargs):
    res = dict()
    collection = kwargs['collection']
    folder_name = kwargs['folder_name']
    real_dir = real_directory(collection)
    folder_name = path_join(real_dir, folder_name)
    os.makedirs(folder_name, exist_ok=True)
    res['status'] = 200
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
        elif document[-3:] == 'ann':
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

def delete_new_document(**kwargs):
    res = dict()
    collection = kwargs['collection']
    document = kwargs['document']
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    if os.path.isdir(document):
        shutil.rmtree(document)
    else:
        os.remove(document+'.txt')
        os.remove(document+'.ann')
        if os.path.exists(document+'_func.ann'):
            os.remove(document+'_func.ann')
    return res
