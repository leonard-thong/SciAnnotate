# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy
  @time:    2020/8/19 11:12 PM
  @project: brat
  @file:    dynamicLabeling.py
===========================================
"""

import os
import random

from utils import GLOBAL_LOGGER, COLOR_PICKER
COMMON_CONTEXT = """
if __name__ == "__main__":
    pass
"""

def generate_color_config(name, entities):
    # TODO: Define entities and color config source
    entity_color_items = []
    for entity in entities:
        entity_color_items.append('\n{}\tbgColor:{}'.format(entity, next(COLOR_PICKER)))
    with open('./data/visualCofigs/drawings.conf', 'a') as color_config:
        color_config.write(''.join(entity_color_items))
    os.system('sh ./data/build_visual_conf.sh')

def _add_labeling_function(name, code):
    try:
        with open('./server/src/labelFunctions/{}.py'.format(name), 'w') as f:
            f.write(code)
            f.write(COMMON_CONTEXT)
        with open('./server/src/labelFunctions/index.py', 'a') as f:
            f.write('\nfrom .{} import *'.format(name))
        return {'status': 0}
    except Exception as e:
        return {'status': -1}


def add_labeling_function(**args):
    try:
        name = args['name']
        code = args['function']
        if name is None or code is None:
            raise Exception("INVALID FUNCTION CODE OR NAME")
        return _add_labeling_function(name, code)
    except Exception as e:
        return {'status': -1}


if __name__ == "__main__":
    pass