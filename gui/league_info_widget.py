# coding=utf-8

from PySide2 import QtWidgets
from gui import widgets
from gui.defines import LayoutType


class LeagueInfoWidget(QtWidgets.QWidget):
    def __init__(self, leagueItem, parent):
        super(LeagueInfoWidget, self).__init__(parent)

        self._leagueItem = leagueItem

        self.setupUi()

    def setupUi(self):
        layout = widgets.getConfiguredLayout(LayoutType.VERTICAL.value, parent=self)

        label = QtWidgets.QLabel(self)
        label.setText("league info")

        layout.addWidget(label)
