import random
import os
import hashlib
import time
import json
from config import BASE_DIR, DATA_DIR
from os.path import join as path_join
from os.path import isabs
from annotation import Annotations
from expandLogger import Logger
from tokenise import whitespace_token_boundary_gen
from annotation import (DISCONT_SEP, TEXT_FILE_SUFFIX,
                        AnnotationsIsReadOnlyError, AttributeAnnotation,
                        BinaryRelationAnnotation,
                        DependingAnnotationDeleteError, EquivAnnotation,
                        EventAnnotation, NormalizationAnnotation,
                        OnelineCommentAnnotation, SpanOffsetOverlapError,
                        TextAnnotations, TextBoundAnnotation,
                        TextBoundAnnotationWithText, open_textfile)
from annotator import ModificationTracker
from document import get_document, get_document_with_sentence_offsets
GLOBAL_LOGGER = Logger()

def get_md5_hash(text):
    md5_obj = hashlib.md5()
    md5_obj.update(text.encode('utf-8'))
    hash_code = md5_obj.hexdigest()
    return hash_code


# def generate_color_config(name, entities):
#     md5_obj = hashlib.md5()
#     entity_color_items = []
#     entity_name_set = set()
#     for entity in entities:
#         md5_obj.update("{}_{}".format(name, entity).encode('utf-8'))
#         hash_code = md5_obj.hexdigest()
#         color = '#{}'.format(str(hash_code)[0:6])
#         color = list(color)
#         for i in range(1, 6, 2):
#             if '9' >= color[i] >= '0':
#                 color[i] = str(hex(int(color[i]) % 5 + 10)).replace('0x', '') 
#         color = ''.join(color)
#         entity_color_items.append('\n{}_{}\tbgColor:{}'.format(name, entity, color))
#         entity_name_set.add('{}_{}'.format(name, entity))
#     entity_color_items.append('\n{}_unlabeled\tbgColor:#000000'.format(name))
#     # TODO: Bug requiring further fix
#     with open('./data/visualConfigs/drawing.conf', 'r') as drawing_content:
#         lines = drawing_content.readlines()
#         for line in lines:
#             entity_name = line.split('\t')[0]
#             if entity_name not in entity_name_set:
#                 entity_color_items.append('\n{}'.format(line))
    
#     if not os.path.exists('./data/visualConfigs/drawings.conf'):
#         with open('./data/visualConfigs/drawings.conf', 'w') as color_config:
#             color_config.write(''.join(entity_color_items))
#     else:
#        with open('./data/visualConfigs/drawings.conf', 'a') as color_config:
#             color_config.write(''.join(entity_color_items)) 
#     os.system('sh ./data/build_visual_conf.sh')

def get_entity_index():
    index = 0
    while 1:
        index += 2
        yield index


def get_entity_index_exist(indexNo):
    index = indexNo
    index = index + 1 if index % 2 == 1 else index
    while 1:
        index += 2
        yield index

def get_entity_index_exist_normal(indexNo):
    index = indexNo
    index = index - 1  if index % 2 == 0 else index -2
    while 1:
        index += 2
        yield index

def clean_cached_config():
    os.system('rm ./data/visualConfigs/drawings.conf')

def add_common_info(text, res):
    res["text"] = text
    res["token_offsets"] = [o for o in whitespace_token_boundary_gen(text)]
    res["ctime"] = time.time()
    res["source_files"] = ["ann", "txt"]
    return res
'''
def get_entity_index_exist(indexNo):
    index = indexNo
    while 1:
        index += 1
        yield index
'''

def annotation_file_generate(out, file_path, text, mode='w'):
    """ Generate ann file content
    """
    file_path = file_path[:-4]
    mods = ModificationTracker()
    with TextAnnotations(file_path) as ann_obj:
        for idx, entity in enumerate(out['entities']):
            new_id = ann_obj.get_new_id('F')
            ann = TextBoundAnnotationWithText(entity[2], new_id, entity[1], entity[3])
            ann_obj.add_annotation(ann)
            mods.addition(ann)

def fetch_all_annotations(**kwargs):
    collection = kwargs['collection']
    document = kwargs['document']
    return get_document(collection, document)


def real_directory(directory, rel_to=DATA_DIR):
    assert isabs(directory), 'directory "%s" is not absolute' % directory
    return path_join(rel_to, directory[1:])

def prehandle_data(**kwargs):
    collection = kwargs['collection']
    document = kwargs['document']
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.txt'
    ann_file_path = txt_file_path[:-4] + '.ann'
    out = []
    doc = get_document_with_sentence_offsets(collection, document)
    entities = doc['entities']
    sentent_offsets = doc['sentence_offsets']
    res = dict()
    res['processedData'] = []
    res['labels'] = []
    res['sources'] = []
    for sentence_offset in sentent_offsets:
        sentence = dict()
        sentence['sentence'] = doc['text'][sentence_offset[0]:sentence_offset[1]]
        sentence['annotation'] = []
        for entity in entities:
            if entity[0][0] == 'F': 
                continue
            if entity[2][0][1] <= sentence_offset[1] and entity[2][0][0] >= sentence_offset[0]:
                source_label = entity[1].split('_')
                source = ''
                label = source_label[0]
                if len(source_label) == 1:
                    source = ''
                    label = source_label[0]
                else:
                    source = source_label[0]
                    label = source_label[1]
                if label not in res['labels']:
                    res['labels'].append(label)
                if source not in res['sources']:
                    res['sources'].append(source)
                sentence['annotation'].append([source, label, entity[2][0][0] - sentence_offset[0], entity[2][0][1] - sentence_offset[0]])
        res['processedData'].append(sentence)
    return res

def _prehandle_data(out, txt_file_path, ann_file_path):
    res = dict()
    with open(ann_file_path, 'r') as ann_file:
        for line in ann_file.readlines():
            if line[0] != 'T' and line[0] != 'F':
                continue
            line_num = -1
            sentence = dict()
            sentence['sentence'] = ''
            sentence['annotation'] = []
            data = []
            line = line.replace('\t', ' ')
            info = line.split(' ')
            source_name = info[1].split('_')[0]
            temp = info[1].split('_')[1:]
            label = ''
            if len(temp) == 0 or source_name.capitalize() == source_name:
                label = info[1]
                source_name = 'spam'
            else:
                for i in range(len(temp)):
                    label += temp[i]
            data.append(source_name)
            data.append(label)
            start = int(info[2])
            end = int(info[3])
            line_dict = judge_line(txt_file_path)
            line_start_index = [key for key in line_dict]
            line_start_index = sorted(line_start_index)
            for i in range(len(line_start_index)):
                if start > int(line_start_index[i]) and end < (int(line_start_index[i]) + len(line_dict[line_start_index[i]])):
                    sentence['sentence']=line_dict[line_start_index[i]]
                    start -= int(line_start_index[i])
                    end -= int(line_start_index[i])
                    line_num = i
                    break
                '''
                elif start > line_start_index[i] and end > (line_start_index[i] + len(line_dict[line_start_index[i]])):
                '''
            data.append(start)
            data.append(end)
            out[line_num]['annotation'].append(data)
    res['processedData'] = out
    return res


def judge_line(txt_file_path):
    count = 0
    line_dict = dict()
    with open(txt_file_path, 'r') as txt_file:
        for line in  txt_file.readlines():
            line_dict[count] = line
            count += len(line)
    return line_dict


def parse_annotation_file(ann_path):
    anns = Annotations(document=ann_path[:-4])
    anns._parse_ann_file()
    return anns._lines

def merge_ann_files(collection, document, append_mode=False):
    file_path = "data" + collection + '/' + document
    manual_anno_file_path = file_path + ".ann"
    label_function_anno_file_path = file_path + "_func.ann"
    if not os.path.exists(label_function_anno_file_path):
        os.system("touch " + label_function_anno_file_path)
    label_func_anno = parse_annotation_file(label_function_anno_file_path)
    label_func_entities = []
    label_func_entities_index = 0
    for ann in label_func_anno:
        try:
            if ann:
                label_func_entities.append([ann.id, ann.type, ann.spans])
                label_func_entities_index += 2
        except AttributeError:
            pass
    manual_anno = parse_annotation_file(manual_anno_file_path)
    manual_entities = []
    manual_entities_index = 1
    for ann in manual_anno:
        try:
            if ann:
                manual_entities.append([ann.id, ann.type, ann.spans])
                manual_entities_index += 2
        except AttributeError:
            pass
    ann_entities = []
    ann_entities.extend(manual_entities)
    ann_entities.extend(label_func_entities)
    if append_mode:
        return label_func_entities
    return ann_entities

def cache_model_results(**kwargs):
    res = dict()
    collection = kwargs['collection']
    document = kwargs['document']
    real_dir = real_directory(collection)
    document = path_join(real_dir, document)
    model_results = json.loads(kwargs['data'])
    
    model_resutls_entities = model_results['entities']
    model_resutls_entities = [[results[0], results[1], results[2][0]] for results in model_resutls_entities]
    with TextAnnotations(document) as ann_obj:
        manual_lines = list(ann_obj.get_entities())
        manual_results = []
        for line in manual_lines:
            if line.id[0] == 'T':
                manual_results.append([line.id, line.type, [line.start, line.end]])
        acc = calc_accuracy(manual_results, model_resutls_entities)
    res['acc'] = acc
    return res

def get_accuray(collection, document):
    real_dir = real_directory(collection)
    document = path_join(real_dir, document)
    acc = 0
    with TextAnnotations(document) as ann_obj:
        all_lines = list(ann_obj.get_entities())
        manual_results = []
        model_results = []
        for line in all_lines:
            if line.id[0] == 'T':
                manual_results.append([line.id, line.type, [line.start, line.end]])
            if line.id[0] == 'F':
                model_results.append([line.id, line.type, [line.start, line.end]])
        acc = calc_accuracy(manual_results, model_results, True)
    return acc

def calc_accuracy(ann_manual, ann_model, soft=False):
    # ['T1', 'label',  (start, end), 'text']
    manual_length = len(ann_manual)
    ann_manual_dict = {"({},{})".format(offset[0], offset[1]):label for _, label, offset in ann_manual}
    ann_model_dict = {"({},{})".format(offset[0], offset[1]):label for _, label, offset in ann_model}

    correct_count = 0
    for key, val in ann_manual_dict.items():
        if key in ann_model_dict.keys():
            if ann_model_dict[key] == val or (soft and val in ann_model_dict[key]):
                correct_count += 1
            else:
                GLOBAL_LOGGER.log_error(key + ' ' + val + ' ' + ann_model_dict[key])
        else:
            GLOBAL_LOGGER.log_error(key + ' ' + val)
    
    return correct_count / manual_length
    
if __name__ == "__main__":
    merge_ann_files('/Local', 'test')