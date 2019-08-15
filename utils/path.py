# coding=utf-8

import os


def getFileExt(filePath):
    return os.path.splitext(filePath)[1]
