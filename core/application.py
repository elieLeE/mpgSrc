# coding=utf-8

from PySide2 import QtCore
from core.application_manager import ApplicationManager


class CoreApplication(object):
    def __init__(self):
        super(CoreApplication, self).__init__()
        self._qApp = self._createQApplication()

        self._applicationManager = None

    def getApplicationManager(self):
        return self._applicationManager

    @staticmethod
    def _createQApplication():
        if QtCore.QCoreApplication.instance() is not None:
            return QtCore.QCoreApplication.instance()
        return QtCore.QCoreApplication()

    def initialize(self):
        self._applicationManager = ApplicationManager()

    def startApp(self):
        self._qApp.exec_()
