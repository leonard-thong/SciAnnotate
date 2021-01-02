# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy
  @time:    2020/8/19 11:12 PM
  @project: dlmat
  @file:    labelMatchEngine.py
===========================================
"""

import re

MATCH_ENGINE_HANDLERS = {
    'keywords': 'keywordHandler',
    'length': 'lengthHandler',
    'regex': 'regexHandler',
}


def mainEngineHandler(match_type, all, **kwargs):
    pass