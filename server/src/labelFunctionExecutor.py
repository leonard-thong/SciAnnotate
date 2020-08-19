# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy
  @time:    2020/8/11 5:20 PM
  @project: brat
  @file:    labelFunctionExecutor.py
===========================================
"""
import re
import sys
import time

from expandLogger import Logger
# from os.path import join as path_join
# from shutil import rmtree
# from tempfile import mkdtemp
#
# from annotation import Annotations, open_textfile
# from document import _document_json_dict
from labelFunctions.index import *
from tokenise import whitespace_token_boundary_gen

GLOBAL_LOGGER = Logger()


def add_common_info(text, res):
    res["text"] = text
    res["token_offsets"] = [o for o in whitespace_token_boundary_gen(text)]
    res["ctime"] = time.time()
    res["source_files"] = ["ann", "txt"]
    return res


def get_entity_index():
    for i in range(1, 1000000):
        yield i


ENTITY_INDEX = get_entity_index()


class Preprocessor(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def process(self, txt):
        out = self.func(txt)
        if out is None:
            GLOBAL_LOGGER.log_warning("WARNING: RETURN VALUE IS NONE")
        return out


def _function_executor(collection, document, functions):
    file_path = "data" + collection + document + ".txt"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        try:
            out = eval(functions[0] + '(content, ENTITY_INDEX)')
            if len(functions) > 1:
                for function in functions[1:]:
                    out['entities'].extend(eval(function + '(content)')['entities'])
                    out['events'].extend(eval(function + '(content)')['events'])
        except Exception as e:
            GLOBAL_LOGGER.log_error("ERROR OCCURRED WHEN PROCESSING LABEL FUNCTION => " + e.__str__())
        if out is not None:
            return add_common_info(content, out)
        else:
            GLOBAL_LOGGER.log_warning("RETURN OF LABEL FUNCTION IS NONE")
    return None


def function_executor(**args):
    GLOBAL_LOGGER.log_normal(args.__str__())
    collection = args["collection"]
    document = args["document"]
    GLOBAL_LOGGER.log_normal(list(args["function[]"]).__str__())
    functions = list(args["function[]"])
    if collection is None:
        GLOBAL_LOGGER.log_error("INVALID DIRECTORY")
    elif document is None:
        GLOBAL_LOGGER.log_error("INVALID DOCUMENT, CANNOT FETCH DOCUMENT")

    out = _function_executor(collection, document, functions)
    out["document"] = document
    out["collection"] = collection
    if out is None:
        return
    return out


def _instant_executor(code, name, entity_index, collection, document):
    file_path = "data" + collection + document + ".txt"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        try:
            exec(code)
            out = eval('{}(content, entity_index)'.format(name))
            return out
        except Exception as e:
            GLOBAL_LOGGER.log_error("ERROR WHILE HANDLING INSTANT REQUEST")


def instant_executor(**args):
    # TODO: implement code completion and return logic
    """
    This function is designed to handle instant labeling function code. The code must be written in a strict format,
    which will be released in a later version README.md .
    :param args: dict | Required arguments set
    :return: dict | Formatted return value with entities, relation and other common info
    """
    collection = args["collection"]
    document = args["document"]
    function_codes = list(args["function"])
    pass


def main(argv):
    pass


if __name__ == "__main__":
    pass

