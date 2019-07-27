# coding=utf-8

from PySide2 import QtCore, QtWidgets
from core import application


class GuiApplication(application.CoreApplication):
    def __init__(self):
        super(GuiApplication, self).__init__()

        self._mainWindow = None

    @staticmethod
    def _createQApplication():
        if QtCore.QCoreApplication.instance():
            if not isinstance(QtCore.QCoreApplication.instance(), QtWidgets.QApplication):
                raise RuntimeError("Cannot create GUI Application, non-GUI application already exists")
            return QtCore.QCoreApplication.instance()
        else:
            return QtWidgets.QApplication([])

    def initialize(self):
        super(GuiApplication, self).initialize()


