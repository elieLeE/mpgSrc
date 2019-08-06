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

    @staticmethod
    def convertMPGDataBaseFile(srcPath, desPath, champName, dayNumber):
        converting.DataFileConverting.convertDataBaseFile(srcPath, desPath, champName, dayNumber)

    def createNewLeague(self, leagueName):
        self._leagues.append(League(leagueName))
