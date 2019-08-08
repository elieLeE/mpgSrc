# coding=utf-8

from PySide2 import QtWidgets


class LeagueInfoWidget(QtWidgets.QWidget):
    def __init__(self, leagueItem, parent):
        super(LeagueInfoWidget, self).__init__(parent)

        self._leagueItem = leagueItem

        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel(self)
        label.setText("league info")

        layout.addWidget(label)
