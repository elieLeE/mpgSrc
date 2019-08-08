# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui


class MercatoWidget(QtWidgets.QWidget):
    def __init__(self, leagueItem, parent):
        super(MercatoWidget, self).__init__(parent)

        self._leagueItem = leagueItem

        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel(self)
        label.setText("Mercato page")
        layout.addWidget(label)
