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

from expandLogger import Logger

# from os.path import join as path_join
# from shutil import rmtree
# from tempfile import mkdtemp
#
# from annotation import Annotations, open_textfile
# from document import _document_json_dict
# from labelFunctions.index import *
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


class Preprocessor(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def process(self, txt):
        out = self.func(txt)
        if out is None:
            GLOBAL_LOGGER.log_warning("WARNING: RETURN VALUE IS NONE")
        return out


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
    file_path = "data" + collection + document
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


def function_executor(**args):
    GLOBAL_LOGGER.log_normal(args.__str__())
    collection = args["collection"]
    document = args["document"]
    GLOBAL_LOGGER.log_normal(list(args["function[]"]).__str__())
    if type(args["function[]"]) == str:
        args["function[]"] = [args["function[]"]]
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


def _instant_executor(code, name, collection, document):
    file_path = "data" + collection + document + ".txt"
    ENTITY_INDEX = get_entity_index()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        try:
            exec(code)
            out = eval("{}(content, ENTITY_INDEX)".format(name))
            if out is not None:
                return add_common_info(content, out)
        except Exception as e:
            GLOBAL_LOGGER.log_error("ERROR WHILE HANDLING INSTANT REQUEST")


def instant_executor(**args):
    """
    This function is designed to handle instant labeling function code. The code must be written in a strict format,
    which will be released in a later version README.md .
    :param args: dict | Required arguments set
    :return: dict | Formatted return value with entities, relation and other common info
    """
    collection = args["collection"]
    document = args["document"]
    if args["function"] is None:
        GLOBAL_LOGGER.log_error("FUNCTION CODE IS NONE")
    else:
        function_code = str(args["function"])
        name = str(args["name"])
        out = _instant_executor(function_code, name, collection, document)
        return out


def main(argv):
    pass


if __name__ == "__main__":
    pass
