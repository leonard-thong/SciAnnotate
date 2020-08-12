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

EXCEPTION = "\033[95mEXCEPTION: "
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93mWARNING: "
ERROR = "\033[91mERROR: "
ENDC = "\033[0m\n"


class Logger(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.f_out = open(self.file_path, "a", encoding="utf8")

    def __del__(self):
        self.f_out.close()

    def log(self, content):
        self.f_out.write(content)

    @staticmethod
    def print(content):
        os.system("echo " + content)

    def log_normal(self, log):
        self.print(OKGREEN + "RUNNING LOG: " + log)

    def log_warning(self, log):
        self.print(WARNING + log + ENDC)

    def log_error(self, log):
        self.print(ERROR + log + ENDC)

    def log_exception(self, log):
        self.print(EXCEPTION + log + ENDC)

    def log_custom(self, style, log):
        self.print(style + log + ENDC)


if __name__ == "__main__":
    logger = Logger("log.txt")
    logger.log_warning("THIS IS A TEST MESSAGE")
    logger.log_normal("THIS IS A TEST MESSAGE")
    logger.log_error("THIS IS A TEST MESSAGE")
