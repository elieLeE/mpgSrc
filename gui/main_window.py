# coding=utf-8

from PySide2 import QtWidgets
from gui.central_widget import CentralWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, application, parent=None):
        super(MainWindow, self).__init__(parent)

        self._application = application

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(self._application.getName())

        centralWidget = CentralWidget(self)
        self.setCentralWidget(centralWidget)

