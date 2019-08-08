# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui


class MercatoWidget(QtWidgets.QWidget):
    def __init__(self, leagueItem, parent):
        super(MercatoWidget, self).__init__(parent)

        self._leagueItem = leagueItem

        self.setupUi()

    def setupUi(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        toolbar = QtWidgets.QToolBar(self.tr("Tool bar"), self)
        toolbar.setStyleSheet("QToolBar {background-color: grey;}")
        toolbar.setMovable(False)

        chooseDataBase = toolbar.addAction("Choose data base")
        chooseDataBase.triggered.connect(self._chooseDataBase)

        addMercatoTurn = toolbar.addAction("Add mercato turn")
        addMercatoTurn.triggered.connect(self._addMercatoTurn)

        mainLayout.addWidget(toolbar)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.setStyleSheet("QSplitter::handle {background-color: black;}")
        splitter.addWidget(ViewDataBaseWidget(self))
        splitter.addWidget(TeamWidget(self))
        mainLayout.addWidget(splitter)

    def _chooseDataBase(self):
        print("chooseDataBase")

    def _addMercatoTurn(self):
        print("mercato turn")


class Widget(QtWidgets.QLabel):
    def __init__(self, text, parent):
        super(Widget, self).__init__(parent)
        self.setText(text)


class ViewDataBaseWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ViewDataBaseWidget, self).__init__(parent)

        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(DataBaseTreeView(self))


class DataBaseTreeView(QtWidgets.QTreeView):
    def __init__(self, parent):
        super(DataBaseTreeView, self).__init__(parent)

        self._model = QtGui.QStandardItemModel()
        self.setModel(self._model)

        self._model.setHorizontalHeaderLabels(["Column 1"])

        self.populate()

    def populate(self):
        self._model.appendRow(QtGui.QStandardItem("test"))


class TeamWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(TeamWidget, self).__init__(parent)

        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(TeamTreeView(self))


class TeamTreeView(QtWidgets.QTreeView):
    def __init__(self, parent):
        super(TeamTreeView, self).__init__(parent)

        self._model = QtGui.QStandardItemModel()
        self.setModel(self._model)

        self._model.setHorizontalHeaderLabels(["Column 1"])

        self.populate()

    def populate(self):
        self._model.appendRow(QtGui.QStandardItem("Gaols"))
        self._model.appendRow(QtGui.QStandardItem("Def"))
        self._model.appendRow(QtGui.QStandardItem("Mil"))
        self._model.appendRow(QtGui.QStandardItem("Att"))
