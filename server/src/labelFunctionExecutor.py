# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy, leonard
  @time:    2020/8/11 5:20 PM
  @project: brat
  @file:    labelFunctionExecutor.py
===========================================
"""
import re
import sys
import time
import os
import logging

from utils import get_entity_index, clean_cached_config, add_common_info, merge_ann_files, GLOBAL_LOGGER, annotation_file_generate


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
    anno_file_path = file_path + "_func.ann"
    ENTITY_INDEX = get_entity_index()
    with open(txt_file_path, "r", encoding="utf-8") as f:
        content = f.read()
        try:
            exec("from labelFunctions.index import {}".format(functions[0]))
            out = eval(functions[0] + "(content, ENTITY_INDEX)")
            if len(functions) > 1:
                for function in functions[1:]:
                    exec("from labelFunctions.index import {}".format(function))
                    out["entities"].extend(
                        eval(function + "(content, ENTITY_INDEX)")["entities"]
                    )
            # out["entities"] = resort_entities(out["entities"], functions)
            annotation_file_generate(out, anno_file_path, content)
        except Exception as e:
            GLOBAL_LOGGER.log_error(
                "ERROR OCCURRED WHEN PROCESSING LABEL FUNCTION => " + e.__str__()
            )
        if out is not None:
            ann_entities = merge_ann_files(collection, document)
            out["entities"] = ann_entities
            #out = out.add(ann_entities)
            return add_common_info(content, out)
        else:
            GLOBAL_LOGGER.log_warning("RETURN OF LABEL FUNCTION IS NONE")
    return None


def function_executor(**kwargs):
    GLOBAL_LOGGER.log_normal(kwargs.__str__())
    collection = kwargs["collection"]
    document = kwargs["document"]
    if type(kwargs["function[]"]) == str:
        kwargs["function[]"] = [kwargs["function[]"]]
    functions = list(kwargs["function[]"])
    if collection is None:
        GLOBAL_LOGGER.log_error("INVALID DIRECTORY")
    elif document is None:
        GLOBAL_LOGGER.log_error("INVALID DOCUMENT, CANNOT FETCH DOCUMENT")
    clean_cached_config()
    out = _function_executor(collection, document, functions)
    out["document"] = document
    out["collection"] = collection
    if out is None:
        return
    return out


def _instant_executor(code, name, collection, document):
    ann_entities = merge_ann_files(collection, document)
    file_path = "./data" + collection + '/' + document + ".txt"
    ENTITY_INDEX = get_entity_index()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        try:
            code = str(code)
            exec(code)
            out = eval("{}(content, ENTITY_INDEX)".format(name))
            if out is not None:
                #out = out.add(ann_entities)
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
