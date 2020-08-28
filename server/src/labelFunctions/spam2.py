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
from utils import generate_color_config

def spam2(text="", entity_index=None):
    entity_list = ['Location', 'Person']
    generate_color_config('spam2', entity_list)
    res = dict()
    entities = [
        ["T" + str(next(entity_index)), "spam2_Location", [(pos.start(), pos.end())]]
        for pos in re.finditer("year", text)
    ]
    entities.extend(
        [
            ["T" + str(next(entity_index)), "spam2_Person", [(pos.start(), pos.end())]]
            for pos in re.finditer("doctor", text)
        ]
    )
    res["entities"] = entities
    return res

if __name__ == "__main__":
    pass
