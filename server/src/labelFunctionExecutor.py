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
from toolBELogger import Logger

GLOBAL_LOGGER = Logger("log.txt")

LABELING_FUNCTION_SET = {
}

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
    file_path = directory + '/' + document

    return None

def function_executor(**args):
    directory = args['collection']
    document = args['document']
    function = LABELING_FUNCTION_SET[args['function']]

    if directory is None:
        GLOBAL_LOGGER.log_error("INVALID DIRECTORY")
    elif document is None:
        GLOBAL_LOGGER.log_error("INVALID DOCUMENT, CANNOT FETCH DOCUMENT")

    out = _function_executor(directory, document, function)

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
