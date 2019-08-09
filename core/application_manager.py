# coding=utf-8

from core import converting
from model.league import League


class ApplicationManager(object):
    def __init__(self):
        super(ApplicationManager, self).__init__()

        self._leagues = []
        self._databases = {}

    @staticmethod
    def getName():
        return "MPG Helper"

    def allActualDataBAse(self):
        return self._databases

    @staticmethod
    def convertMPGDataBaseFile(srcPath, desPath, champName, dayNumber):
        converting.DataFileConverting.convertDataBaseFile(srcPath, desPath, champName, dayNumber)

    def createNewLeague(self, leagueName):
        newLeagueItem = League(leagueName)
        self._leagues.append(newLeagueItem)
        return newLeagueItem
