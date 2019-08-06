# coding=utf-8


class League(object):
    def __init__(self, leagueName):
        super(League, self).__init__()

        self._leagueName = leagueName
        self._dataBase = None
        self._mercato = None
