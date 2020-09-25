import re
from os.path import join as path_join
from os.path import split as path_split
from jsonwrap import dumps as json_dumps
from jsonwrap import loads as json_loads
from annotation import TEXT_FILE_SUFFIX,JOINED_ANN_FILE_SUFF
from utils import get_entity_index_exist
from document import real_directory
from os.path import join as path_join

def create_span_all(collection, document, label_word):
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.' + TEXT_FILE_SUFFIX
    ann_file_path = JOINED_ANN_FILE_SUFF + '.' + JOINED_ANN_FILE_SUFF
    return _create_span_all(txt_file_path,label_word, ann_file_path)


def _create_span_all(txt_file_path, label_word, ann_file_path, entity_index = get_entity_index_exist):
    res = dict()
    with open_textfile(txt_file_path, 'r') as txt_file:
        text = txt_file.read()
    with open_textfile(ann_file_path, 'r') as ana_file:
        ann = ann_file.readlines()
    for line in ann:
        entity_index = line.split(" ")
        entity_index = entity_index[0][1:] 
    
    entity_index = get_entity_index_exist(entity_index)

    entities = [
        ["T" + str(next(entity_index)), "Location", [(pos.start(), pos.end())]]
        for pos in re.finditer(label_word, text)
    ]
    res["entities"] = entities
    return entities

def create_span_with_re(collection, document, regx):
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.' + TEXT_FILE_SUFFIX
    ann_file_path = JOINED_ANN_FILE_SUFF + '.' + JOINED_ANN_FILE_SUFF
    return _create_span_regx(txt_file_path,ann_file_path, regx)

def _create_span_regx(txt_file_path, ann_file_path, regx):
    res = dict()
    with open_textfile(txt_file_path, 'r') as txt_file:
        text = txt_file.read()
    with open_textfile(ann_file_path, 'r') as ana_file:
        ann = ann_file.readlines()
    for line in ann:
        entity_index = line.split(" ")
        entity_index = entity_index[0][1:]
    
    entity_index = get_entity_index_exist(entity_index)
    regx = re.compile(regx)
    entities = [
        ["T" + str(next(entity_index)), "Location", [(pos.start(), pos.end())]]
        for pos in regx.finditer(text)
    ]
    res["entities"] = entities
    return entities