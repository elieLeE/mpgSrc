# coding=utf-8

from PySide2 import QtCore, QtWidgets
from core import application
from gui import main_window
from gui import window_manager


class GuiApplication(application.CoreApplication):
    def __init__(self):
        super(GuiApplication, self).__init__()

        self._windowManager = None

    def getWindowManager(self):
        return self._windowManager

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
        self._windowManager = window_manager.WindowManager(self)
        # self._windowManager.registerMainWindow(main_window.MainWindow(self))
