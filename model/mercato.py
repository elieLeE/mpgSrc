# coding=utf-8

import weakref


class Mercato(object):
    def __init__(self):
        super(Mercato, self).__init__()

        self._dataBase = None

    def getDataBase(self):
        if self._dataBase is None:
            return None
        return self._dataBase()

    def setDataBase(self, dataBaseInst):
        self._dataBase = weakref.ref(dataBaseInst)
