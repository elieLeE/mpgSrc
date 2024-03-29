# coding=utf-8

from utils import path
from core import data_reader
from core import converting
from core.defines import EXT_FILES
from model.league import League
from model.data_base import DataBase


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

    def loadDataBaseInLeague(self, leagueInst, dataBasePath):
        dataBaseInst = self._databases.get(dataBasePath, None)
        if dataBaseInst is not None:
            leagueInst.setDataBase(dataBaseInst)
        else:
            dataBaseInst = DataBase("", "")
            data_reader.readDataBase(dataBasePath, dataBaseInst)
            self._databases[dataBasePath] = dataBaseInst
        return dataBaseInst
