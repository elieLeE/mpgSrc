# coding=utf-8
from builtins import super

from PySide2 import QtWidgets, QtCore, QtGui
import re
from enum import Enum
import pickle
from core.defines import Position
from gui.tree_view import TreeView
from gui.defines import MimeTypes, UserRoles


class Filters(Enum):
    NAME = "Name"
    POSITION = "Pos"
    TEAMS = "Teams"
    PRIZE = "Prize"
    EVAL = "Eval"
    TIT = "Tit"
    GOALS = "Goals"
    SELECTION = "Select"

    @staticmethod
    def getDefaultVal(filterVal):
        if filterVal in [Filters.NAME.value, Filters.POSITION.value, Filters.TEAMS.value]:
            return ""
        if filterVal in [Filters.PRIZE.value, Filters.EVAL.value, Filters.TIT.value, Filters.GOALS.value]:
            return -1
        return False


class ViewDataBaseWidget(QtWidgets.QWidget):
    def __init__(self, dataBaseInst, parent):
        super(ViewDataBaseWidget, self).__init__(parent)
        self._dataBaseInst = dataBaseInst

        self._dictFilters = {Filters.NAME.value: Filters.getDefaultVal(Filters.NAME.value),
                             Filters.POSITION.value: Filters.getDefaultVal(Filters.POSITION.value),
                             Filters.TEAMS.value: Filters.getDefaultVal(Filters.TEAMS.value),
                             Filters.PRIZE.value: Filters.getDefaultVal(Filters.PRIZE.value),
                             Filters.EVAL.value: Filters.getDefaultVal(Filters.EVAL.value),
                             Filters.TIT.value: Filters.getDefaultVal(Filters.TIT.value),
                             Filters.GOALS.value: Filters.getDefaultVal(Filters.GOALS.value),
                             Filters.SELECTION.value: Filters.getDefaultVal(Filters.SELECTION.value)}

        self._filterWidget = None
        self._dataBaseTreeView = None

        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)

        self._filterWidget = FilterWidget(self._dataBaseInst, self._dictFilters, self)
        layout.addWidget(self._filterWidget)

        self._dataBaseTreeView = DataBaseTreeView(self._dataBaseInst, self._dictFilters, self)
        layout.addWidget(self._dataBaseTreeView)

        self._filterWidget.filterChanged.connect(self._dataBaseTreeView.updateFiltering)

    def updateWidget(self, dataBaseInst):
        self._dataBaseInst = dataBaseInst
        self._filterWidget.updateWidget(dataBaseInst)
        self._dataBaseTreeView.updateTree(dataBaseInst)

    def selectPlayerItem(self, playerId):
        self._dataBaseTreeView.selectPlayerItem(playerId)


class FilterWidget(QtWidgets.QWidget):
    filterChanged = QtCore.Signal()

    def __init__(self, dataBaseInst, dictFilters, parent):
        super(FilterWidget, self).__init__(parent)

        self._dictFilters = dictFilters

        self._playerNameEdit = None
        self._selectionCheckBox = None
        self._teamComboBox = None
        self._posComboBox = None
        self._prizeComboBox = None
        self._evalComboBox = None
        self._titComboBox = None
        self._goalsNumberComboBox = None
        self._dataBaseTreeView = None

        self.setupUi()
        self._fillComboBoxes(dataBaseInst)

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)

        horizontalLayout = QtWidgets.QHBoxLayout()
        self._playerNameEdit = QtWidgets.QLineEdit(self)
        self._playerNameEdit.setPlaceholderText("Nom joueur")
        self._playerNameEdit.textChanged.connect(self._playerNameEditChanged)
        horizontalLayout.addWidget(self._playerNameEdit)

        self._teamComboBox = QtWidgets.QComboBox(self)
        self._teamComboBox.currentIndexChanged.connect(lambda: self._comboBoxChanged(self._teamComboBox,
                                                                                     Filters.TEAMS.value))
        # self._teamComboBox.setStyleSheet("color: rgb(160, 160, 164);")
        # self._teamComboBox.setStyleSheet("QComboBox { background-color: white; color: rgb(160, 160, 164) }" "QListView { color: black; }")
        # self._teamComboBox.setStyleSheet("QComboBox { combobox-popup: 0; color: white; padding: 0px 0px 0px 0px}")
        horizontalLayout.addWidget(self._teamComboBox)

        self._posComboBox = QtWidgets.QComboBox(self)
        self._posComboBox.currentIndexChanged.connect(lambda: self._comboBoxChanged(self._posComboBox,
                                                                                    Filters.POSITION.value))
        # self._posComboBox.setStyleSheet("color: rgb(160, 160, 164);")
        horizontalLayout.addWidget(self._posComboBox)

        label = QtWidgets.QLabel(self)
        label.setText("Selection")
        horizontalLayout.addWidget(label)
        self._selectionCheckBox = QtWidgets.QCheckBox(self)
        self._selectionCheckBox.stateChanged.connect(self._selectionCheckBoxChanged)
        horizontalLayout.addWidget(self._selectionCheckBox)

        horizontalLayout2 = QtWidgets.QHBoxLayout()

        self._prizeComboBox = QtWidgets.QComboBox(self)
        self._prizeComboBox.currentIndexChanged.connect(lambda: self._comboBoxChanged(self._prizeComboBox,
                                                                                      Filters.PRIZE.value))
        # self._prizeComboBox.setStyleSheet("color: rgb(160, 160, 164);")
        horizontalLayout2.addWidget(self._prizeComboBox)

        self._evalComboBox = QtWidgets.QComboBox(self)
        self._evalComboBox.currentIndexChanged.connect(lambda: self._comboBoxChanged(self._evalComboBox,
                                                                                     Filters.EVAL.value))
        # self._evalComboBox.setStyleSheet("color: rgb(160, 160, 164);")
        horizontalLayout2.addWidget(self._evalComboBox)

        self._titComboBox = QtWidgets.QComboBox(self)
        self._titComboBox.currentIndexChanged.connect(lambda: self._comboBoxChanged(self._titComboBox,
                                                                                    Filters.TIT.value))
        # self._titComboBox.setStyleSheet("color: rgb(160, 160, 164);")
        horizontalLayout2.addWidget(self._titComboBox)

        self._goalsNumberComboBox = QtWidgets.QComboBox(self)
        self._goalsNumberComboBox.currentIndexChanged.connect(lambda: self._comboBoxChanged(self._goalsNumberComboBox,
                                                                                            Filters.GOALS.value))
        # self._goalsNumberComboBox.setStyleSheet("color: rgb(160, 160, 164);")
        horizontalLayout2.addWidget(self._goalsNumberComboBox)

        layout.addLayout(horizontalLayout)
        layout.addLayout(horizontalLayout2)

    def _fillComboBoxes(self, dataBaseInst):
        def _fillInfComboBox(comboBoxInst, base, itemsList, filterId):
            comboBoxInst.addItem(base, Filters.getDefaultVal(filterId))
            for item in itemsList:
                comboBoxInst.addItem("{} {}".format(base, str(item)), item)

        self._posComboBox.addItems(["Pos"] + [p.value for p in list(Position)])

        _fillInfComboBox(self._evalComboBox, "Eval Moy Sup. à", list(range(4, 9, 1)), Filters.EVAL.value)
        _fillInfComboBox(self._goalsNumberComboBox, "Nbre Buts Sup. à", list(range(5, 31, 5)), Filters.GOALS.value)
        _fillInfComboBox(self._prizeComboBox, "Prix inf. à", list(range(10, 41, 10)), Filters.PRIZE.value)
        _fillInfComboBox(self._titComboBox, "% Tit Sup. à", list(range(40, 101, 10)), Filters.TIT.value)

        if dataBaseInst is not None:
            self._fillDataBaseComboBox(dataBaseInst)

    def _fillDataBaseComboBox(self, dataBaseInst):
        self._teamComboBox.addItems(["Clubs"] + [t.getId() for t in dataBaseInst.getAllTeams()])

    def _comboBoxChanged(self, comboBoxInst, filterId):
        if comboBoxInst.currentIndex() == 0:
            self._dictFilters[filterId] = Filters.getDefaultVal(filterId)
        elif filterId in [Filters.POSITION.value, Filters.TEAMS.value]:
            self._dictFilters[filterId] = comboBoxInst.currentText()
        else:
            self._dictFilters[filterId] = comboBoxInst.currentData()

        self.filterChanged.emit()

    def _playerNameEditChanged(self):
        self._dictFilters[Filters.NAME.value] = self._playerNameEdit.text()
        self.filterChanged.emit()

    def _selectionCheckBoxChanged(self):
        self._dictFilters[Filters.SELECTION.value] = (self._selectionCheckBox.checkState() == QtCore.Qt.Checked)
        self.filterChanged.emit()

    def updateWidget(self, dataBaseInst):
        self._fillDataBaseComboBox(dataBaseInst)


class DataBaseTreeViewColumn(Enum):
    SELECTION = 0, "Selection"
    NAME = SELECTION[0] + 1, "Name"
    POSITION = NAME[0] + 1, "Poste"
    TEAM = POSITION[0] + 1, "Equipe"
    EVAL_MOY = TEAM[0] + 1, "Note Moy"
    GAOL_NUMBER = EVAL_MOY[0] + 1, "Buts"
    PRIZE = GAOL_NUMBER[0] + 1, "Cote"
    PERCENT_TIT = PRIZE[0] + 1, "Titulaire"


class DataBaseTreeView(TreeView):
    def __init__(self, dataBaseInst, dictFilters, parent):
        super(DataBaseTreeView, self).__init__(DataBaseTreeViewColumn, parent)

        self._dataBaseInst = dataBaseInst

        self._dictFilters = dictFilters

        sourceModel = DataBaseTreeModel()
        proxyModel = DataBaseTreeSortFilterModel(self._dictFilters)
        proxyModel.setSourceModel(sourceModel)
        self.setModel(proxyModel)

        self.setDragEnabled(True)

    def _populate(self):
        if self._dataBaseInst is not None:
            for playerInst in self._dataBaseInst.getAllPlayers():
                self.sourceModel().appendRow(self._getNewPlayerItemsList(playerInst))

    def _getNewPlayerItemsList(self, playerInst):
        playerItemsList = self._getNewItemsList(DataBasePlayerItem, playerInst)
        playerItemsList[DataBaseTreeViewColumn.SELECTION.value[0]].setCheckable(True)
        return playerItemsList

    def updateTree(self, dataBaseInst):
        self._dataBaseInst = dataBaseInst

        self.sourceModel().clear()

        self._populate()
        self.refresh()

    def updateFiltering(self):
        self.model().applyFilters()
        self.refresh()

    def selectPlayerItem(self, playerId):
        itemsIndex = self._getItems(UserRoles.ID_ROLE.value, playerId)
        if len(itemsIndex) == 1:
            sourceIndex = self.model().mapToSource(itemsIndex[0])
            playerItem = self.sourceModel().itemFromIndex(sourceIndex)
            if playerItem is not None:
                playerItem.selectItem()


class DataBaseTreeSortFilterModel(QtCore.QSortFilterProxyModel):
    def __init__(self, dictFilters):
        super(DataBaseTreeSortFilterModel, self).__init__()
        self._dictFilters = dictFilters

        self.setDynamicSortFilter(True)

    def applyFilters(self):
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        sourceParent = self.mapToSource(sourceParent)
        indexItem = self.sourceModel().index(sourceRow, 0, sourceParent)
        playerItem = self.sourceModel().itemFromIndex(indexItem)

        if playerItem is None:
            return True

        playerData = playerItem.getPlayerData()

        nameFilter = self._dictFilters[Filters.NAME.value]
        if nameFilter != Filters.getDefaultVal(Filters.NAME.value) \
                and re.search(nameFilter, playerData.getName(), re.IGNORECASE) is None:
            return False

        teamFilter = self._dictFilters[Filters.TEAMS.value]
        if teamFilter != Filters.getDefaultVal(Filters.TEAMS.value) and teamFilter != playerData.getTeam().getId():
            return False

        playerGlobalPos = Position.getGloBasPos(playerData.getPosition())
        posFilter = self._dictFilters[Filters.POSITION.value]
        if posFilter != Filters.getDefaultVal(Filters.POSITION.value)\
                and (posFilter != playerGlobalPos) and (posFilter != playerData.getPosition()):
            return False

        if self._dictFilters[Filters.SELECTION.value] and not playerItem.getSelectStatus():
            return False

        prizeFilter = int(self._dictFilters[Filters.PRIZE.value])
        if prizeFilter != -1 and playerData.getOffPrize() > prizeFilter:
            return False

        evalFilter = int(self._dictFilters[Filters.EVAL.value])
        if evalFilter != -1 and playerData.getEval() < evalFilter:
            return False

        goalsFilter = int(self._dictFilters[Filters.GOALS.value])
        if goalsFilter != -1 and playerData.getGoalNumber() < goalsFilter:
            return False

        titFilter = int(self._dictFilters[Filters.TIT.value])
        if titFilter != -1 and playerData.getPercentTit() < titFilter:
            return False

        return True

    def data(self, index, role):
        if role == QtCore.Qt.BackgroundRole:
            if index.row() % 2 == 0:
                return QtGui.QColor(226, 237, 253)
            return QtCore.Qt.white
        return super(DataBaseTreeSortFilterModel, self).data(index, role)


class DataBaseTreeModel(QtGui.QStandardItemModel):
    def __init__(self):
        super(DataBaseTreeModel, self).__init__()
        self._setHeader()

    def _setHeader(self):
        self.setHorizontalHeaderLabels([v.value[1] for v in list(DataBaseTreeViewColumn)])

    def mimeData(self, indexes):
        """Return an object that contains serialized items of data corresponding to the list of indexes specified.
        The formats used to describe the encoded data is obtained from the mimeTypes() function.

        :param indexes: QModelIndex instance. represent the index of the item in the treeView we want to DAD.
        :return: QMimeData instance
        """
        mimeData = QtCore.QMimeData()
        playerInst = indexes[0].model().itemFromIndex(indexes[0]).getPlayerData()
        data = pickle.dumps({"playerData": playerInst})
        mimeData.setData(MimeTypes.PLAYER.value, data)
        return mimeData

    def clear(self):
        super(DataBaseTreeModel, self).clear()
        self._setHeader()


class DataBasePlayerItem(QtGui.QStandardItem):
    def __init__(self, playerDataInst):
        super(DataBasePlayerItem, self).__init__()
        self._playerDataInst = playerDataInst

        self.setEditable(False)

    def data(self, role):
        if role == QtCore.Qt.DisplayRole:
            if self.column() == DataBaseTreeViewColumn.NAME.value[0]:
                return self._playerDataInst.getName()
            if self.column() == DataBaseTreeViewColumn.POSITION.value[0]:
                return self._playerDataInst.getPosition()
            if self.column() == DataBaseTreeViewColumn.TEAM.value[0]:
                return self._playerDataInst.getTeam().getId()
            if self.column() == DataBaseTreeViewColumn.EVAL_MOY.value[0]:
                return self._playerDataInst.getEval()
            if self.column() == DataBaseTreeViewColumn.GAOL_NUMBER.value[0]:
                return self._playerDataInst.getGoalNumber()
            if self.column() == DataBaseTreeViewColumn.PRIZE.value[0]:
                return self._playerDataInst.getOffPrize()
            if self.column() == DataBaseTreeViewColumn.PERCENT_TIT.value[0]:
                return "{} %".format(self._playerDataInst.getPercentTit())
        elif role == UserRoles.ID_ROLE.value:
            return self._playerDataInst.getId()

        return super(DataBasePlayerItem, self).data(role)

    def getPlayerData(self):
        return self._playerDataInst

    def selectItem(self):
        self.setCheckState(QtCore.Qt.Checked)

    def getSelectStatus(self):
        return self.data(QtCore.Qt.CheckStateRole)
