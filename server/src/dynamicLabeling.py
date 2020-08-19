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

COMMON_CONTEXT = """
if __name__ == "__main__":
    pass
"""


def add_labeling_function(name, code):
    try:
        with open('./labelFunctions/{}.py'.format(name), 'w') as f:
            f.write(code)
            f.write(COMMON_CONTEXT)

        with open('./labelFunctions/index.py', 'a') as f:
            f.write('\nfrom {} import *'.format(name))
        return {'status': 0}
    except Exception as e:
        return {'status': -1}

if __name__ == "__main__":
    pass