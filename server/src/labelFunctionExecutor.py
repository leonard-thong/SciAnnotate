# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy, leonard
  @time:    2020/8/11 5:20 PM
  @project: dlmat
  @file:    labelFunctionExecutor.py
===========================================
"""
import re
import sys
import time
import os
import logging

from utils import get_entity_index, clean_cached_config, add_common_info, merge_ann_files, GLOBAL_LOGGER
from annotation import (DISCONT_SEP, TEXT_FILE_SUFFIX,
                        AnnotationsIsReadOnlyError, AttributeAnnotation,
                        BinaryRelationAnnotation,
                        DependingAnnotationDeleteError, EquivAnnotation,
                        EventAnnotation, NormalizationAnnotation,
                        OnelineCommentAnnotation, SpanOffsetOverlapError,
                        TextAnnotations, TextBoundAnnotation,
                        TextBoundAnnotationWithText, open_textfile)
from annotator import ModificationTracker
from document import get_document
def resort_entities(entity_list, func_name_list):
    all_entities = dict()
    ENTITY_INDEX = get_entity_index()
    for entity in entity_list:
        if all_entities.get(entity[2][0]):
            all_entities[entity[2][0]].append(entity[1])
        else:
            all_entities[entity[2][0]] = [entity[1]]
    for key, labels in all_entities.items():
        new_labels = []
        for idx, func_name in enumerate(func_name_list):
            found = False
            for label in labels:
                if func_name == label.split('_')[0]:
                    new_labels.append(label)
                    found = True
                    break
            if not found:
                new_labels.append('{}_unlabeled'.format(func_name))
        all_entities[key] = new_labels
    out = []
    for idx in range(func_name_list.__len__()):
        for key, labels in all_entities.items():
            out.append(["T{}".format(next(ENTITY_INDEX)), labels[idx], [key]])
    return out

    

def _function_executor(collection, document, functions):
    file_path = "data" + collection + '/' + document
    txt_file_path = file_path + ".txt"
    try:
        content = None
        with open(txt_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        ENTITY_INDEX = get_entity_index()
        exec("from labelFunctions.index import {}".format(functions[0]))
        out = eval(functions[0] + "(content, ENTITY_INDEX)")
        if len(functions) > 1:
            for function in functions[1:]:
                exec("from labelFunctions.index import {}".format(function))
                out["entities"].extend(
                    eval(function + "(content, ENTITY_INDEX)")["entities"]
                )
        mods = ModificationTracker()
        with TextAnnotations(file_path) as ann_obj:
            new_id = ann_obj.get_new_id('F')
            for i in range(1, int(new_id[1:])):
                ann = ann_obj.get_ann_by_id('F{}'.format(i))
                ann_obj.del_annotation(ann, mods)
            for idx, entity in enumerate(out['entities']):
                new_id = ann_obj.get_new_id('F')
                ann = TextBoundAnnotationWithText(entity[2], new_id, entity[1], entity[3])
                ann_obj.add_annotation(ann)
                mods.addition(ann)
                out['entities'][idx][0] = new_id
        return add_common_info(content, out)
    except Exception as e:
        GLOBAL_LOGGER.log_error(
            "ERROR OCCURRED WHEN PROCESSING LABEL FUNCTION => " + e.__str__()
        )

def get_label_scope(collection, scope):
    scope_list = []
    if scope == "currentCollection":
        # currentCollection
        for root, dirs, files in os.walk("./data{}".format(collection), topdown=True):
            for name in files:
                if name.split('.')[-1] == 'txt':
                    scope_list.append(['{}/'.format(root[6:]), name[:-4]])
    elif scope == "allCollections":
        # allCollection
        for _, dirs, _ in os.walk("./data", topdown=True):
            for dir_name in dirs:
                for root, dir2, files in os.walk("./data/{}".format(dir_name), topdown=True):
                    for file_name in files:
                        if file_name.split('.')[-1] == 'txt':
                            scope_list.append(['{}/'.format(root[6:]), file_name[:-4]])
    return scope_list

def function_executor(**kwargs):
    GLOBAL_LOGGER.log_normal(kwargs.__str__())
    collection = kwargs["collection"]
    document = kwargs["document"]
    scope = kwargs["scope[]"] if kwargs['scope[]'] else "currentDocument"
    if type(kwargs["function[]"]) == str:
            kwargs["function[]"] = [kwargs["function[]"]]
    functions = list(kwargs["function[]"])
    out = dict()
    if collection is None:
        GLOBAL_LOGGER.log_error("INVALID DIRECTORY")
    elif document is None:
        GLOBAL_LOGGER.log_error("INVALID DOCUMENT, CANNOT FETCH DOCUMENT")
    if scope not in ['currentCollection', 'allCollections']:
        clean_cached_config()
        out = _function_executor(collection, document, functions)
    else:
        operation_scope_list = get_label_scope(collection, scope)
        clean_cached_config()
        for single_apply in operation_scope_list:
            if single_apply[1] == document:
                out = _function_executor(single_apply[0], single_apply[1], functions)
            else:
                _function_executor(single_apply[0], single_apply[1], functions)
    out["document"] = document
    out["collection"] = collection
    if out is None:
        return
    return get_document(collection, document)


def _instant_executor(code, name, collection, document):
    file_path = "./data" + collection + '/' + document + ".txt"
    ENTITY_INDEX = get_entity_index()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        try:
            code = str(code)
            exec(code)
            out = eval("{}(content, ENTITY_INDEX)".format(name))
            if out is not None:
                return add_common_info(content, out)
        except Exception as e:
            logging.exception(str(e))
            GLOBAL_LOGGER.log_error("ERROR WHILE HANDLING INSTANT REQUEST")


def instant_executor(**kwargs):
    """
    This function is designed to handle instant labeling function code. The code must be written in a strict format,
    which will be released in a later version README.md .
    :param kwargs: dict | Required arguments set
    :return: dict | Formatted return value with entities, relation and other common info
    """
    collection = kwargs["collection"]
    document = kwargs["document"]
    if kwargs["function"] is None:
        GLOBAL_LOGGER.log_error("FUNCTION CODE IS NONE")
    else:
        clean_cached_config()
        function_code = str(kwargs["function"])
        name = str(kwargs["name"])
        name_start = 0
        for code_line in function_code.split('\n'):
            if code_line[0:3] == "def":
                name_start = 4
                for i in range(4, 100):
                    if code_line[i] == "(":
                        name_end = i
                        break
                name = code_line[name_start:name_end]
                break
        out = _instant_executor(function_code, name, collection, document)
        return out


if __name__ == "__main__":
    pass
