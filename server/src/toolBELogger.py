# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy
  @time:    2020/8/11 5:54 PM
  @project: brat
  @file:    toolBELogger.py
===========================================
"""
import sys
import os

EXCEPTION = "\033[95m"
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
ERROR = "\033[91m"
ENDC = "\033[0m"


class Logger(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def log(self, content):
        f_out = open(self.file_path, 'a', encoding='utf8')
        f_out.write(content)
        f_out.close()
        os.system('clear')
        os.system('cat log.txt')

    def log_normal(self, log):
        self.log(log)

    def log_warning(self, log):
        self.log(WARNING + log + ENDC)

    def log_error(self, log):
        self.log(ERROR + log + ENDC)

    def log_exception(self, log):
        self.log(EXCEPTION + log + ENDC)

    def log_custom(self, style, log):
        self.log(style + log + ENDC)


if __name__ == '__main__':
    pass
