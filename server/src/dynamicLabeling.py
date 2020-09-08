# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy. leonard
  @time:    2020/8/19 11:12 PM
  @project: brat
  @file:    dynamicLabeling.py
===========================================
"""

import os

from utils import GLOBAL_LOGGER
COMMON_CONTEXT = """
if __name__ == "__main__":
    pass
"""

def _add_labeling_function(name, code):
    try:
        with open('./server/src/labelFunctions/{}.py'.format(name), 'w') as f:
            f.write(code)
            f.write(COMMON_CONTEXT)
        with open('./server/src/labelFunctions/index.py', 'r+') as f:
            if 'from .{} import *'.format(name) not in f.read():
                f.write(f.read())
                f.write('\nfrom .{} import *'.format(name))
        with open('./data/labelingFunctionList.conf', 'r+') as f:
            current_list = f.read().split('\n')
            if name in current_list:
                pass
            else:
                f.write('\n{}'.format(name))
        return {'status': 0}
    except Exception as e:
        GLOBAL_LOGGER.log_exception(e.__str__())
        return {'status': -1}


def add_labeling_function(**args):
    try:
        name = args['name']
        code = args['function']
        if name is None or code is None:
            raise Exception("INVALID FUNCTION CODE OR NAME")
        return _add_labeling_function(name, code)
    except Exception as e:
        GLOBAL_LOGGER.log_exception(e.__str__())
        return {'status': -1}


def _delete_labeling_function(function_list):
    try:
        for function in function_list:
            # delete python file
            if os.path.exists('./server/src/labelFunctions/{}.py'.format(function)):
                os.remove('./server/src/labelFunctions/{}.py'.format(function))
            else:
                continue

            # delete import in index.py
            with open("./server/src/labelFunctions/index.py", "r") as f:
                lines = f.readlines()
            with open("./server/src/labelFunctions/index.py", "w") as f:
                for line in lines:
                    if line != "":
                        if line.strip("\n") != "from .{} import *".format(function):
                            f.write(line)

            # delete labeling function in labelingFunctionList.conf
            with open("./data/labelingFunctionList.conf", "r") as f:
                lines = f.readlines()
            with open("./data/labelingFunctionList.conf", "w") as f:
                for line in lines:
                    if line != "":
                        if line.strip("\n") != function:
                            f.write(line)

            return {'status': 0}
    except Exception as e:
        GLOBAL_LOGGER.log_exception(e.__str__())
        return {'status': -1}


def delete_labeling_function(**kwargs):
    try:
        if type(kwargs["function[]"]) == str:
            kwargs["function[]"] = [kwargs["function[]"]]
        function_list = list(kwargs["function[]"])
        if function_list is None:
            raise Exception("INVALID FUNCTION CODE OR NAME")
        return _delete_labeling_function(function_list)
    except Exception as e:
        GLOBAL_LOGGER.log_exception(e.__str__())
        return {'status': -1}


def _get_available_labeling_function(collection=None):
    res = dict()
    # if collection is None:
    with open('./data/labelingFunctionList.conf', 'r') as f:
        content = f.read()
        res['function_list'] = content.split('\n')
    return res


def get_available_labeling_function(**args):
    try:
        collection = args['collection']
        return _get_available_labeling_function(collection)
    except Exception as e:
        GLOBAL_LOGGER.log_exception(e.__str__())


if __name__ == "__main__":
    pass