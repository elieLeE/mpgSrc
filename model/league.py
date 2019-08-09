# coding=utf-8

from model.data_base import DataBase

class League(object):
    def __init__(self, leagueName):
        super(League, self).__init__()

        self._leagueName = leagueName
        self._dataBase = DataBase("", "")
        self._mercato = None

    def getName(self):
        return self._leagueName

    def getDataBase(self):
        return self._dataBase
