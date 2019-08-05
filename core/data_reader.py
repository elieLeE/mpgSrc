# coding=utf-8

import csv
import re
import xml.etree.cElementTree as xmlElt
from core.defines import XML
from core.players import Player
from core.teams import Team


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
                    playersList.append(Player(idPlayer, playerName, pos, eval, int(gaolNumber), int(prize), percentTit))

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
                    playerId = playerElt.get('id')
                    playerName = playerElt.get('name')
                    pos = playerElt.get('pos')
                    eval = float(playerElt.get('eval'))
                    goalNumber = int(playerElt.get('goalNumber'))
                    prize = int(playerElt.get('prize'))
                    percentTit = float(playerElt.get('percentTit'))
                    dataBaseInst.addPlayer(Player(playerId, playerName, pos, eval,
                                                  goalNumber, prize, percentTit, newTeam))
