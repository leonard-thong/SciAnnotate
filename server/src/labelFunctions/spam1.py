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


def spam1(text="", entity_index=None):
    res = dict()
    entities = [
        ["T" + str(next(entity_index)), "time", [(pos.start(), pos.end())]]
        for pos in re.finditer("year", text)
    ]
    entities.extend(
        [
            ["T" + str(next(entity_index)), "Person", [(pos.start(), pos.end())]]
            for pos in re.finditer("million", text)
        ]
    )
    entities.extend(
        [
            ["T" + str(next(entity_index)), "NoneType", [(pos.start(), pos.end())]]
            for pos in re.finditer("was", text)
        ]
    )
    res["entities"] = entities
    return res

if __name__ == "__main__":
    pass