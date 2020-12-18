import re
from document import real_directory, get_document
from os.path import join as path_join
from os.path import join as path_join
from os.path import split as path_split
from jsonwrap import dumps as json_dumps
from jsonwrap import loads as json_loads
from utils import get_entity_index_exist_normal, add_common_info, annotation_file_generate,parse_annotation_file, merge_ann_files,clean_cached_config, GLOBAL_LOGGER
from labelFunctionExecutor import get_label_scope


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
    GLOBAL_LOGGER.log_normal(kwargs.__str__())
    collection = kwargs["collection"]
    document = kwargs["document"]
    label = kwargs['label']
    keyword = kwargs['keyword']
    scope = kwargs["scope[]"] if kwargs['scope[]'] else "currentDocument"
    out = dict()
    if collection is None:
        GLOBAL_LOGGER.log_error("INVALID DIRECTORY")
    elif document is None:
        GLOBAL_LOGGER.log_error("INVALID DOCUMENT, CANNOT FETCH DOCUMENT")
    if scope not in ['currentCollection', 'allCollections']:
        clean_cached_config()
        directory = collection
        real_dir = real_directory(directory)
        doc = path_join(real_dir, document)
        txt_file_path = doc + '.txt'
        ann_file_path = txt_file_path[:-4] + '.ann'
        out = _create_span_all_text(txt_file_path, ann_file_path, keyword, label, kwargs)
    else:
        operation_scope_list = get_label_scope(collection, scope)
        clean_cached_config()
        for single_apply in operation_scope_list:
            directory = single_apply[0]
            real_dir = real_directory(directory)
            doc = path_join(real_dir, single_apply[1])
            txt_file_path = doc + '.txt'
            ann_file_path = txt_file_path[:-4] + '.ann'
            if single_apply[1] == document:
                out = _create_span_all_text(txt_file_path, ann_file_path, keyword, label, kwargs)
            else:
                _create_span_all_text(txt_file_path, ann_file_path, keyword, label, kwargs)
    out["document"] = document
    out["collection"] = collection
    if out is None:
        return
    return get_document(collection, document)

def _create_span_all_text(txt_file_path, ann_file_path, keyword, label, kwargs, entity_index = get_entity_index_exist_normal):
    collection = kwargs['collection']   
    document = kwargs['document']

    res = dict()
    with open(txt_file_path, 'r') as txt_file:
        text = txt_file.read()
    with open(ann_file_path, 'r') as ann_file:
        ann = ann_file.read()

    exist_index = ann.split('\n').__len__()
    
    entity_index = get_entity_index_exist_normal(exist_index)

    location = locations_of_substring(text.lower(),keyword.lower())
    entities = [
        ["F" + str(next(entity_index)), label, [(pos, pos + len(keyword))], text[pos:pos + len(keyword)]]
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
    return res

def create_span_all_re(**kwargs):
    GLOBAL_LOGGER.log_normal(kwargs.__str__())
    collection = kwargs["collection"]
    document = kwargs["document"]
    label = kwargs['label']
    keyword = kwargs['keyword']
    scope = kwargs["scope[]"] if kwargs['scope[]'] else "currentDocument"
    out = dict()
    if collection is None:
        GLOBAL_LOGGER.log_error("INVALID DIRECTORY")
    elif document is None:
        GLOBAL_LOGGER.log_error("INVALID DOCUMENT, CANNOT FETCH DOCUMENT")
    if scope not in ['currentCollection', 'allCollections']:
        clean_cached_config()
        directory = collection
        real_dir = real_directory(directory)
        doc = path_join(real_dir, document)
        txt_file_path = doc + '.txt'
        ann_file_path = txt_file_path[:-4] + '.ann'
        out = _create_span_all_re(txt_file_path, ann_file_path, keyword, label, kwargs)
    else:
        operation_scope_list = get_label_scope(collection, scope)
        clean_cached_config()
        for single_apply in operation_scope_list:
            directory = single_apply[0]
            real_dir = real_directory(directory)
            doc = path_join(real_dir, single_apply[1])
            txt_file_path = doc + '.txt'
            ann_file_path = txt_file_path[:-4] + '.ann'
            if single_apply[1] == document:
                out = _create_span_all_re(txt_file_path, ann_file_path, keyword, label, kwargs)
            else:
                _create_span_all_re(txt_file_path, ann_file_path, keyword, label, kwargs)
    out["document"] = document
    out["collection"] = collection
    if out is None:
        return
    return get_document(collection, document)

def _create_span_all_re(txt_file_path, ann_file_path, keyword, label, kwargs):
    collection = kwargs['collection']   
    document = kwargs['document']

    res = dict()
    with open(txt_file_path, 'r') as txt_file:
        text = txt_file.read()
    with open(ann_file_path, 'r') as ann_file:
        ann = ann_file.read()

    exist_index = ann.split('\n').__len__()
    
    entity_index = get_entity_index_exist_normal(exist_index)

    location = locations_of_substring(text,keyword)
    
    entities = [
        ["F" + str(next(entity_index)), label, [(pos.start(), pos.end())], text[pos:pos + len(keyword)]]
        for pos in re.finditer(keyword, text)
    ]
    
    res["entities"] = entities
    annotation_file_generate(res, ann_file_path, text, 'a')
    return res