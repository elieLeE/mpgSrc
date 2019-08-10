# coding=utf-8

import weakref


class League(object):
    def __init__(self, leagueName):
        super(League, self).__init__()

        self._leagueName = leagueName
        # self._dataBase = DataBase("", "")
        self._dataBase = None
        self._mercato = None

    def getName(self):
        return self._leagueName

    def getDataBase(self):
        if self._dataBase is None:
            return None
        return self._dataBase()

    def setDataBase(self, dataBaseInst):
        self._dataBase = weakref.ref(dataBaseInst)
