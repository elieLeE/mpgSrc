# coding=utf-8

import csv
import re
from core.players import Player
from core.teams import Team


class FileReader(object):
    def __init__(self, filePath):
        self._filePath = filePath


class MPGDataBaseFileReader(FileReader):
    def __init__(self, filePath):
        super(MPGDataBaseFileReader, self).__init__(filePath)

    def read(self, dataBaseInst):
        teamsPlayers = {}

        with open(self._filePath, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    idPlayer, pos, idTeam, eval, gaolNumber, prize, percentTit = row
                except:
                    print("here")
                if idPlayer != "":
                    playersList = teamsPlayers.get(idTeam, [])
                    if len(playersList) == 0:
                        teamsPlayers[idTeam] = playersList
                    eval = float(eval.replace(",", "."))
                    percentTit = float(re.sub(r"\s*%", "", percentTit).replace(",", "."))
                    playersList.append(Player(idPlayer, pos, eval, int(gaolNumber), int(prize), percentTit))

            for idTeam, playersList in teamsPlayers.items():
                newTeam = Team(idTeam)
                dataBaseInst.addTeam(newTeam)
                for playerInst in playersList:
                    playerInst.setTeam(newTeam)
                    dataBaseInst.addPlayer(playerInst)
