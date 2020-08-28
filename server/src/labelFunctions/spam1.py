# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy
  @time:    2020/8/19 11:06 PM
  @project: brat
  @file:    spam1.py
===========================================
"""
import re
from utils import generate_color_config

def spam1(text="", entity_index=None):
    entity_list = ['Location', 'NoneType']
    generate_color_config('spam1', entity_list)
    res = dict()
    entities = [
        ["T" + str(next(entity_index)), "spam1_Location", [(pos.start(), pos.end())]]
        for pos in re.finditer("year", text)
    ]
    entities.extend(
        [
            ["T" + str(next(entity_index)), "spam1_NoneType", [(pos.start(), pos.end())]]
            for pos in re.finditer("was", text)
        ]
    )
    res["entities"] = entities
    return res

if __name__ == "__main__":
    pass