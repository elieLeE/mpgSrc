# coding=utf-8

from PySide2 import QtWidgets, QtCore
from gui import widgets
from gui.defines import LayoutType
from gui.dialogs import GetPathMercatoTurnDialog
from gui.team_widget import TeamWidget
from gui.data_base_widget import ViewDataBaseWidget


class MercatoWidget(QtWidgets.QWidget):
    def __init__(self, mercatoInst, parent):
        super(MercatoWidget, self).__init__(parent)

        self._mercatoInst = mercatoInst

        self._viewDataBaseWidget = None

        self.setupUi()

    def setupUi(self):
        mainLayout = widgets.getConfiguredLayout(LayoutType.VERTICAL.value, parent=self)

        toolbar = QtWidgets.QToolBar(self.tr("Tool bar"), self)
        toolbar.setStyleSheet("QToolBar {background-color: grey;}")
        toolbar.setMovable(False)

        addMercatoTurn = toolbar.addAction("Add mercato turn")
        addMercatoTurn.triggered.connect(self._addMercatoTurn)

        mainLayout.addWidget(toolbar)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.setStyleSheet("QSplitter::handle {background-color: black;}")
        self._viewDataBaseWidget = ViewDataBaseWidget(self._mercatoInst.getDataBase(), self)
        splitter.addWidget(self._viewDataBaseWidget)
        teamWidget = TeamWidget(self)
        splitter.addWidget(teamWidget)
        mainLayout.addWidget(splitter)

        teamWidget.newPlayerDropped.connect(self._viewDataBaseWidget.selectPlayerItem)

    def update(self):
        self._viewDataBaseWidget.updateWidget(self._mercatoInst.getDataBase())

    def _addMercatoTurn(self):
        print("mercato turn")

        dialog = GetPathMercatoTurnDialog(self)
        ret = dialog.exec_()
