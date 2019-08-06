# coding=utf-8

from PySide2 import QtWidgets, QtCore

from gui.central_widget import CentralWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, application, parent=None):
        super(MainWindow, self).__init__(parent)

        self._application = application

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(self._application.getApplicationManager().getName())

        centralWidget = CentralWidget(self)
        self.setCentralWidget(centralWidget)

        toolbar = QtWidgets.QToolBar(self.tr("Tool bar"), self)
        toolbar.setMovable(False)

        convertDataBaeAction = toolbar.addAction("Create new league")
        convertDataBaeAction.triggered.connect(self._application.getWindowManager().createNewLeague)

        loadLeagueAction = toolbar.addAction("Load league")
        loadLeagueAction.setDisabled(True)

        toolbar.addSeparator()

        convertDataBaeAction = toolbar.addAction("Convert data base")
        convertDataBaeAction.triggered.connect(self._application.getWindowManager().convertMPGDataBase)

        self.addToolBar(toolbar)
