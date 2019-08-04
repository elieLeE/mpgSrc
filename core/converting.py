# coding=utf-8

import os
from core.data_base import DataBase
from core import data_reader
from core import data_writer


class DataFileConverting(object):
    def __init__(self):
        super(DataFileConverting, self).__init__()

    @staticmethod
    def convertDataBaseFile(srcPath, desPath, champName, dayNumber):
        desFileData = os.path.basename(srcPath).split('.')
        desPath = os.path.join(desPath, str(desFileData[0]) + '.xml')

        print("convertDataBaseFile")
        if not os.path.exists(srcPath):
            raise Exception("Path {} is not valid".format(srcPath))

        if os.path.exists(desPath):
            raise Exception("Path {} already exist".format(desPath))

        dataBaseInst = DataBase(champName, dayNumber)
        data_reader.MPGDataBaseFileReader(srcPath).read(dataBaseInst)
        data_writer.GlobalDataBaseFileWriter(desPath).write(dataBaseInst)

