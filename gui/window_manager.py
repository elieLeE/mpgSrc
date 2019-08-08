# coding=utf-8

from PySide2 import QtWidgets
from gui.dialogs import ConvertFileDialog, NewLeagueDialog


class WindowManager(object):
    def __init__(self, application):
        super(WindowManager, self).__init__()

        self._application = application
        self._mainWindow = None

    def registerMainWindow(self, mw):
        self._mainWindow = mw

    def convertMPGDataBase(self):
        dialog = ConvertFileDialog(self._mainWindow)
        ret = dialog.exec_()

        if ret == QtWidgets.QDialog.Accepted:
            self._application.getApplicationManager().convertMPGDataBaseFile(dialog.getSrcPath(), dialog.getDesPath(),
                                                                             dialog.getChampName(), dialog.getDayNumber())

        dialog.setParent(None)
        dialog.deleteLater()

    def createNewLeague(self):
        dialog = NewLeagueDialog(self._mainWindow)
        ret = dialog.exec_()

        if ret == QtWidgets.QDialog.Accepted:
            newLeagueItem = self._application.getApplicationManager().createNewLeague(dialog.getLeagueName())
            self._mainWindow.addLeagueItem(newLeagueItem)

        dialog.setParent(None)
        dialog.deleteLater()
