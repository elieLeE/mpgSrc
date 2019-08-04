# coding=utf-8

from PySide2 import QtCore
from core import converting


class CoreApplication(object):
    def __init__(self):
        super(CoreApplication, self).__init__()
        self._qApp = self._createQApplication()

    @staticmethod
    def getName():
        return "MPG Helper"

    @staticmethod
    def _createQApplication():
        if QtCore.QCoreApplication.instance() is not None:
            return QtCore.QCoreApplication.instance()
        return QtCore.QCoreApplication()

    def initialize(self):
        pass

    def startApp(self):
        self._qApp.exec_()

    @staticmethod
    def convertMPGDataBaseFile(srcPath, desPath, champName, dayNumber):
        converting.DataFileConverting.convertDataBaseFile(srcPath, desPath, champName, dayNumber)
