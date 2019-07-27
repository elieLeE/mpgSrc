# coding=utf-8

from PySide2 import QtCore


class CoreApplication(object):
    def __init__(self):
        super(CoreApplication, self).__init__()
        self._qApp = self._createQApplication()

    @staticmethod
    def _createQApplication():
        if QtCore.QCoreApplication.instance() is not None:
            return QtCore.QCoreApplication.instance()
        return QtCore.QCoreApplication()

    def initialize(self):
        pass

    def startApp(self):
        self._qApp.exec_()

