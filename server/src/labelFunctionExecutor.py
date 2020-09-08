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

from utils import GLOBAL_LOGGER
from utils import get_entity_index, clean_cached_config, add_common_info


def annotation_file_generate(res, file_path, text):
    anno_content = ""
    for entity in res["entities"]:
        anno_content += (
            str(entity[0])
            + "\t"
            + str(entity[1])
            + " "
            + str(entity[2][0][0])
            + " "
            + str(entity[2][0][1])
            + "\t"
            + str(text[entity[2][0][0]: entity[2][0][1]])
            + "\n"
        )
    with open(file_path, 'w') as f:
        f.write(anno_content)


def _function_executor(collection, document, functions):
    file_path = "data" + collection + '/' + document
    txt_file_path = file_path + ".txt"
    anno_file_path = file_path + ".ann"
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
            annotation_file_generate(out, anno_file_path, content)
        except Exception as e:
            GLOBAL_LOGGER.log_error(
                "ERROR OCCURRED WHEN PROCESSING LABEL FUNCTION => " + e.__str__()
            )
        if out is not None:
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
        out = _instant_executor(function_code, name, collection, document)
        return out


if __name__ == "__main__":
    pass
