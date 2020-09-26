import re
from document import real_directory
from os.path import join as path_join
from os.path import join as path_join
from os.path import split as path_split
from jsonwrap import dumps as json_dumps
from jsonwrap import loads as json_loads
from utils import get_entity_index_exist, get_entity_index, add_common_info, annotation_file_generate,parse_annotation_file


def locations_of_substring(string, substring):
    """Return a list of locations of a substring."""

    substring_length = len(substring)    
    def recurse(locations_found, start):
        location = string.find(substring, start)
        if location != -1:
            return recurse(locations_found + [location], location+substring_length)
        else:
            return locations_found

    return recurse([], 0)



def create_span_all_text(**kwargs):
    label = kwargs['label']
    collection = kwargs['collection']
    document = kwargs['document']
    keyword = kwargs['keyword']
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.txt'
    ann_file_path = txt_file_path[:-3] + 'ann'
    return _create_span_all_text(txt_file_path, ann_file_path, keyword, label)

def _create_span_all_text(txt_file_path, ann_file_path, keyword, label, entity_index = get_entity_index_exist):
    res = dict()
    with open(txt_file_path, 'r') as txt_file:
        text = txt_file.read()
    with open(ann_file_path, 'r') as ann_file:
        ann = ann_file.read()

    exist_index = ann.split('\n').__len__()
    
    entity_index = get_entity_index_exist(exist_index)

    location = locations_of_substring(text,keyword)
    entities = [
        ["T" + str(next(entity_index)), label, [(pos, pos + len(keyword))]]
        for pos in location
    ]
    '''
    entities = [
        ["T" + str(next(entity_index)), label, [(pos.start(), pos.end())]]
        for pos in re.finditer(keyword, text)
    ]
    '''
    res["entities"] = entities
    annotation_file_generate(res, ann_file_path, text, 'a')
    cur_anns = parse_annotation_file(ann_file_path)
    cur_entities = []
    for cur_ann in cur_anns:
        try:
            if cur_ann:
                cur_entities.append([cur_ann.id, cur_ann.type, cur_ann.spans])
        except AttributeError:
            pass
    res['entities'] = cur_entities
    res = add_common_info(text, res)
    
    return res

def create_span_all_re(**kwargs):
    label = kwargs['label']
    collection = kwargs['collection']
    document = kwargs['document']
    keyword = kwargs['label_word']
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.txt'
    ann_file_path = txt_file_path[:-3] + 'ann'
    return _create_span_all_re(txt_file_path, ann_file_path, keyword, label)

def _create_span_regx(txt_file_path, ann_file_path, keyword, label):
    res = dict()
    with open(txt_file_path, 'r') as txt_file:
        text = txt_file.read()
    with open(ann_file_path, 'r') as ann_file:
        ann = ann_file.read()

    exist_index = ann.split('\n').__len__()
    
    entity_index = get_entity_index_exist(exist_index)

    location = locations_of_substring(text,keyword)
    
    entities = [
        ["T" + str(next(entity_index)), label, [(pos.start(), pos.end())]]
        for pos in re.finditer(keyword, text)
    ]
    
    res["entities"] = entities
    annotation_file_generate(res, ann_file_path, text, 'a')
    cur_anns = parse_annotation_file(ann_file_path)
    cur_entities = []
    for cur_ann in cur_anns:
        try:
            if cur_ann:
                cur_entities.append([cur_ann.id, cur_ann.type, cur_ann.spans])
        except AttributeError:
            pass
    res['entities'] = cur_entities
    res = add_common_info(text, res)
    return res