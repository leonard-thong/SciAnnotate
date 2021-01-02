# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy
  @time:    2020/8/11 5:54 PM
  @project: dlmat
  @file:    expandLogger.py
===========================================
"""
import sys
import os

EXCEPTION = "\n\033[95mEXCEPTION: "
OKBLUE = "\n\033[94m"
OKGREEN = "\n\033[92m"
WARNING = "\033[93mWARNING: "
ERROR = "\n\033[91mERROR: "
ENDC = "\033[0m"


class Logger(object):
    # def __init__(self, file_path):
    #     self.file_path = file_path
    #     self.f_out = open(self.file_path, "a", encoding="utf8")

    # def __del__(self):
        # self.f_out.close()

    # def log(self, content):
    #     self.f_out.write(content)

    @staticmethod
    def print(content):
        os.system("echo " + "'" + content.__str__().replace(' ', '\ ').replace('(','\(').replace(')','\)').replace('&','\&') + "'")

    def log_normal(self, log):
        self.print(OKGREEN + "RUNNING LOG: " + log.__str__() + ENDC)

    def log_warning(self, log):
        self.print(WARNING + log.__str__() + ENDC)

    def log_error(self, log):
        self.print(ERROR + log.__str__() + ENDC)

    def log_exception(self, log):
        self.print(EXCEPTION + log.__str__() + ENDC)

    def log_custom(self, style, log):
        self.print(style + log.__str__() + ENDC)


if __name__ == "__main__":
    logger = Logger()
    logger.log_warning("THIS IS A TEST MESSAGE")
    logger.log_normal("THIS IS A TEST MESSAGE")
    logger.log_error("THIS IS A TEST MESSAGE")
