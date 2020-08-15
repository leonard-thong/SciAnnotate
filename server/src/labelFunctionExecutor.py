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
from expandLogger import Logger

GLOBAL_LOGGER = Logger()


def spam(text=""):
    return {'version': 1}


LABELING_FUNCTION_SET = {"spam": spam}


class Preprocessor(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def process(self, txt):
        out = self.func(txt)
        if out is None:
            GLOBAL_LOGGER.log_warning("WARNING: RETURN VALUE IS NONE")
        return out


class PreprocessPipeline(object):
    def __init__(self, processor_list):
        self.processor_list = processor_list

    def process(self, txt, log=False):
        if not log:
            out = txt
            for processor in self.processor_list:
                if type(processor) != Preprocessor:
                    GLOBAL_LOGGER.log_error(
                        "TYPE ERROR: CANNOT USE NONE PREPROCESSOR TO PROCESS DATA"
                    )
                    return None
                out = processor(out)
            return out
        else:
            out = [txt]
            for processor in self.processor_list:
                if type(processor) != Preprocessor:
                    GLOBAL_LOGGER.log_error(
                        "TYPE ERROR: CANNOT USE NONE PREPROCESSOR TO PROCESS DATA"
                    )
                    return None
                out.append(processor(out[-1]))
            return out

    def re_init(self, processor_list):
        self.processor_list = processor_list


def _function_executor(directory, document, function):
    file_path = "data" + directory + document + '.txt'
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        content.replace("\n", "")
        try:
            out = function(content)
        except Exception as e:
            GLOBAL_LOGGER.log_error("ERROR OCCURRED WHEN PROCESSING LABEL FUNCTION")
        if out is not None:
            return out
        else:
            GLOBAL_LOGGER.log_warning("RETURN OF LABEL FUNCTION IS NONE")
    return out


def function_executor(**args):
    GLOBAL_LOGGER.log_normal(args.__str__())
    directory = args["collection"]
    document = args["document"]
    function = LABELING_FUNCTION_SET[args["function"]]

    if directory is None:
        GLOBAL_LOGGER.log_error("INVALID DIRECTORY")
    elif document is None:
        GLOBAL_LOGGER.log_error("INVALID DOCUMENT, CANNOT FETCH DOCUMENT")

    out = _function_executor(directory, document, function)
    if out is None:
        return
    return out


def function_executors(label_function_sets, txt):
    out = []
    for label_function in label_function_sets:
        out.append(label_function(txt))
    return out


def main(argv):
    pass


if __name__ == "__main__":
    sys.exit(main(sys.argv))
