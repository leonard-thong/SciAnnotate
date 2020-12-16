# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy
  @time:    2020/8/19 11:03 PM
  @project: brat
  @file:    spam.py
===========================================
"""
import re
import sys


def spam_get_entities(text, entity_index):
    entities = [
        ["T" + str(next(entity_index)), "quantity", [(pos.start(), pos.end())], text[pos.start(): pos.end()]]
        for pos in re.finditer("million", text)
    ]
    entities.extend(
        [
            ["T" + str(next(entity_index)), "quantity", [(pos.start(), pos.end())], text[pos.start(): pos.end()]]
            for pos in re.finditer("billion", text)
        ]
    )
    entities.extend(
        [
            ["T" + str(next(entity_index)), "money", [(pos.start(), pos.end())], text[pos.start(): pos.end()]]
            for pos in re.finditer("(\$([1-9|.]*))|(dollars)", text)
        ]
    )
    return entities


def spam_get_realtions(text):
    pass


def spam(text="", entity_index=None):
    res = dict()
    entities = spam_get_entities(text, entity_index)
    entity_list = set()
    for index, entity in enumerate(entities):
        entity_list.add(entity[1])
        entities[index][1] = '{}_{}'.format(str(sys._getframe().f_code.co_name), entity[1])
    res["entities"] = entities
    return res

if __name__ == "__main__":
    pass