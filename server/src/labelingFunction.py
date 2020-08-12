# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy
  @time:    2020/8/11 7:03 PM
  @project: brat
  @file:    labelingFunction.py
===========================================
"""


class LabelingFunction(object):
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.func = None

    def implementation(self, func):
        self.func = func


class SPAM(LabelingFunction):
    def __init__(self):
        super(LabelingFunction, self).__init__("SPAM")

    def process(self, x):
        pass


if __name__ == '__main__':
    pass
