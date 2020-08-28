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
COMMON_CONTEXT = """
if __name__ == "__main__":
    pass
"""

def color_generator(num):
    return '0' + str(hex(num)) if num > 0 else str(hex(num))

def random_color_generator():
    while 1:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        yield '#' + color_generator(r) + color_generator(g) + color_generator(b)

COLOR_PICKER = random_color_generator()

def generate_color_config(name, entities):
    entity_color_items = []
    for entity in entities:
        entity_color_items.append('{}\tbgColor:{}'.format(entity, next(COLOR_PICKER)))
    with open('./data/visual.conf', 'w') as f:
        # TODO: Add wirting logic
        pass

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
        return _add_labeling_function(name, code)
    except Exception as e:
        return {'status': -1}


if __name__ == "__main__":
    pass