# coding=utf-8

import xml.etree.cElementTree as xmlElt
# from ElementTree_pretty import prettify


class FileWriter(object):
    def __init__(self, filePath):
        self._filePath = filePath


class GlobalDataBaseFileWriter(FileWriter):
    def __init__(self, filePath):
        super(GlobalDataBaseFileWriter, self).__init__(filePath)

    def write(self, dataBaseInst):
        root = xmlElt.Element('GlobalDataBase')
        root.set('version', '1.0')

        title = xmlElt.SubElement(root, 'champ')
        title.text = dataBaseInst.getChampName()
        dc = xmlElt.SubElement(root, 'dayNumber')
        dc.text = dataBaseInst.getDayNumber()

        for teamInst in dataBaseInst.getAllTeams():
            teamElt = xmlElt.SubElement(root, 'team', {'name': teamInst.getId()})

            for playerInst in teamInst.getAllPlayers():
                xmlElt.SubElement(teamElt, 'player', {'name': playerInst.getId(),
                                                      'pos': playerInst.getPosition(),
                                                      'eval': str(playerInst.getEval()),
                                                      'goalNumber': str(playerInst.getGoalNumber()),
                                                      'prize': str(playerInst.getPrize()),
                                                      'percentTit': str(playerInst.getPercentTit())})

        tree = xmlElt.ElementTree(root)
        tree.write(self._filePath)
