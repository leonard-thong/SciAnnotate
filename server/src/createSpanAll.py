import re
from document import real_directory
from os.path import join as path_join
from os.path import join as path_join
from os.path import split as path_split
from jsonwrap import dumps as json_dumps
from jsonwrap import loads as json_loads
from annotation import TEXT_FILE_SUFFIX,JOINED_ANN_FILE_SUFF, open_textfile
from utils import get_entity_index_exist

#collection, document, keyword, label
def create_span_all_text(**kwargs):
    directory = kwargs["collection"]
    document = kwargs["document"]
    keyword = kwargs["keyword"]
    label = kwargs["label"]
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.' + TEXT_FILE_SUFFIX
    ann_file_path = document + '.' + JOINED_ANN_FILE_SUFF
    return _create_span_all_text(txt_file_path, keyword, label, ann_file_path)


def _create_span_all_text(txt_file_path, keyword, label, ann_file_path, entity_index = get_entity_index_exist):
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
        ["T" + str(next(entity_index)), label, [(pos.start(), pos.end())]]
        for pos in re.finditer(keyword, text)
    ]
    res["entities"] = entities
    return entities

def create_span_all_re(**kwargs):
    directory = kwargs["collection"]
    document = kwargs["document"]
    keyword = kwargs["keyword"]
    label = kwargs["label"]
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.' + TEXT_FILE_SUFFIX
    ann_file_path = document + '.' + JOINED_ANN_FILE_SUFF
    return _create_span_regx(txt_file_path, ann_file_path, keyword, label)

def _create_span_regx(txt_file_path, ann_file_path, keyword, label):
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
        ["T" + str(next(entity_index)), label, [(pos.start(), pos.end())]]
        for pos in regx.finditer(text)
    ]
    res["entities"] = entities
    return entities