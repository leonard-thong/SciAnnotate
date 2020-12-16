# -*- coding:utf-8 -*-
"""
===========================================
  @author:  leonard
  @time:    2020/8/19 10:25 PM
  @project: brat
  @file:    spam2.py
===========================================
"""
import re
import sys


def spam2(text="", entity_index=None):
    res = dict()
    entities = [
        ["T" + str(next(entity_index)), "Location", [(pos.start(), pos.end())]]
        for pos in re.finditer("year", text)
    ]
    entities.extend(
        [
            ["T" + str(next(entity_index)), "Person", [(pos.start(), pos.end())]]
            for pos in re.finditer("doctor", text)
        ]
    )
    entity_list = set()
    for index, entity in enumerate(entities):
        entity_list.add(entity[1])
        entities[index][1] = '{}_{}'.format(str(sys._getframe().f_code.co_name), entity[1])
    res["entities"] = entities
    return res

if __name__ == "__main__":
    pass
