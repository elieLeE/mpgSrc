# coding=utf-8

import xml.etree.cElementTree as xmlElt
from core.defines import XML


class FileWriter(object):
    def __init__(self, filePath):
        self._filePath = filePath


class GlobalDataBaseFileWriter(FileWriter):
    def __init__(self, filePath):
        super(GlobalDataBaseFileWriter, self).__init__(filePath)

    def write(self, dataBaseInst):
        root = xmlElt.Element(XML.ATTR_GLOBAL_DATA_BASE)
        root.set(XML.TAG_VERSION, '1.0')

        title = xmlElt.SubElement(root, XML.ATTR_CHAMP)
        title.text = dataBaseInst.getChampName()
        dc = xmlElt.SubElement(root, XML.ATTR_DAY_NUMBER)
        dc.text = dataBaseInst.getDayNumber()

        for teamInst in dataBaseInst.getAllTeams():
            teamElt = xmlElt.SubElement(root, XML.ATTR_TEAM, {XML.TAG_NAME: teamInst.getId()})

            for playerInst in teamInst.getAllPlayers():
                xmlElt.SubElement(teamElt, XML.ATTR_PLAYER, {XML.TAG_ID: playerInst.getId(),
                                                             XML.TAG_NAME: playerInst.getName(),
                                                             XML.TAG_POSITION: playerInst.getPosition(),
                                                             XML.TAG_EVAL: str(playerInst.getEval()),
                                                             XML.TAG_GOAL_NUMBER: str(playerInst.getGoalNumber()),
                                                             XML.TAG_PRIZE: str(playerInst.getOffPrize()),
                                                             XML.TAG_PERCENT_TIT: str(playerInst.getPercentTit())})

        tree = xmlElt.ElementTree(root)
        tree.write(self._filePath)
