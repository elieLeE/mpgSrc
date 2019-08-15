# coding=utf-8

from model.mercato import Mercato


class League(object):
    def __init__(self, leagueName):
        super(League, self).__init__()

        self._leagueName = leagueName
        # self._dataBase = DataBase("", "")
        self._mercato = Mercato()

    def getName(self):
        return self._leagueName

    def getMercato(self):
        return self._mercato
