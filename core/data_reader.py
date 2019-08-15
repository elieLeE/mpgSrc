# coding=utf-8

import csv
import re
from utils import path
import xml.etree.cElementTree as xmlElt
from core.defines import XML, EXT_FILES
from model.players import Player
from model.teams import Team


def readDataBase(filePath, dataBaseInst):
    ext = path.getFileExt(filePath)
    if ext == EXT_FILES.CSV.value:
        MPGDataBaseCSVFileReader(filePath).read(dataBaseInst)
    elif ext == EXT_FILES.XML.value:
        MPGDataBaseXMLFileReader(filePath).read(dataBaseInst)
    else:
        print("Data base not read. Unknown extension: {}".format(ext))


class FileReader(object):
    def __init__(self, filePath):
        self._filePath = filePath


class MPGDataBaseCSVFileReader(FileReader):
    def __init__(self, filePath):
        super(MPGDataBaseCSVFileReader, self).__init__(filePath)

    def read(self, dataBaseInst):
        teamsPlayers = {}

        with open(self._filePath, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                playerName, pos, idTeam, eval, gaolNumber, prize, percentTit = row
                if playerName != "":
                    playersList = teamsPlayers.get(idTeam, [])
                    if len(playersList) == 0:
                        teamsPlayers[idTeam] = playersList
                    idPlayer = "{}_{}".format(idTeam, playerName)
                    eval = float(eval.replace(",", "."))
                    percentTit = float(re.sub(r"\s*%", "", percentTit).replace(",", "."))
                    playersList.append(Player(idPlayer, playerName, pos, eval, int(gaolNumber), int(prize), int(prize), percentTit))

            for idTeam, playersList in teamsPlayers.items():
                newTeam = Team(idTeam)
                dataBaseInst.addTeam(newTeam)
                for playerInst in playersList:
                    playerInst.setTeam(newTeam)
                    dataBaseInst.addPlayer(playerInst)


class MPGDataBaseXMLFileReader(FileReader):
    def __init__(self, filePath):
        super(MPGDataBaseXMLFileReader, self).__init__(filePath)

    def read(self, dataBaseInst):
        with open(self._filePath) as f:
            tree = xmlElt.parse(self._filePath)
            root = tree.getroot()

            for teamElt in root.iter(XML.ATTR_TEAM):
                newTeam = Team(teamElt.get(XML.TAG_NAME))
                dataBaseInst.addTeam(newTeam)

                for playerElt in teamElt.iter(XML.ATTR_PLAYER):
                    playerId = playerElt.get(XML.TAG_ID)
                    playerName = playerElt.get(XML.TAG_NAME)
                    pos = playerElt.get(XML.TAG_POSITION)
                    evalMoy = float(playerElt.get(XML.TAG_EVAL))
                    goalNumber = int(playerElt.get(XML.TAG_GOAL_NUMBER))
                    offPrize = int(playerElt.get(XML.TAG_PRIZE))
                    buyPrize = int(playerElt.get(XML.TAG_BUY_PRIZE, offPrize))
                    percentTit = float(playerElt.get(XML.TAG_PERCENT_TIT))
                    dataBaseInst.addPlayer(Player(playerId, playerName, pos, evalMoy, goalNumber,
                                                  offPrize, buyPrize, percentTit, newTeam))
