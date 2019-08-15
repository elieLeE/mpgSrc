# coding=utf-8

import os
from PySide2 import QtWidgets
from core.defines import ChampName
from .defines import LayoutType
from gui.widgets import FileBrowserPath, DirectoryBrowserPath, getConfiguredLayout


class SrcDesPathWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(SrcDesPathWidget, self).__init__(parent)

        self._srcPathEdit = None
        self._desPathEdit = None

        self._srcPathWidget = None
        self._desPathWidget = None

        self.setupUi()

    def setupUi(self):
        verticalLayout = getConfiguredLayout(LayoutType.VERTICAL.value, [0], 5, parent=self)

        self._srcPathWidget = FileBrowserPath("Src", self.tr("Files (*.csv)"), self)
        self._srcPathWidget.pathChanged.connect(self._changeSrcPath)

        self._desPathWidget = DirectoryBrowserPath("Des", "", self)

        verticalLayout.addWidget(self._srcPathWidget)
        verticalLayout.addWidget(self._desPathWidget)

    def _changeSrcPath(self, newSrcPath):
        if newSrcPath != "":
            self._desPathWidget.resetPath(os.path.dirname(newSrcPath))

    def getSrcPath(self):
        return self._srcPathWidget.getPathChosen()

    def getDesPath(self):
        return self._desPathWidget.getPathChosen()


class ConvertFileDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(ConvertFileDialog, self).__init__(parent)

        self._srcDesPathWidget = None
        self._comboBoxChamp = None
        self._comboBoxDayNumber = None
        self.setupUi()

        self._fillChampComboBox()
        self._fillDayNumberComboBox()

    def setupUi(self):
        verticalLayout = getConfiguredLayout(LayoutType.VERTICAL.value, parent=self)

        self._srcDesPathWidget = SrcDesPathWidget(self)
        verticalLayout.addWidget(self._srcDesPathWidget)

        horizontalLayoutOpts = getConfiguredLayout(LayoutType.HORIZONTAL.value, margins=[0])
        labelSrc = QtWidgets.QLabel(self)
        labelSrc.setText("Champ")
        horizontalLayoutOpts.addWidget(labelSrc)

        self._comboBoxChamp = QtWidgets.QComboBox(self)
        horizontalLayoutOpts.addWidget(self._comboBoxChamp)

        labelSrc = QtWidgets.QLabel(self)
        labelSrc.setText("Day Number")
        horizontalLayoutOpts.addWidget(labelSrc)

        self._comboBoxDayNumber = QtWidgets.QComboBox(self)
        horizontalLayoutOpts.addWidget(self._comboBoxDayNumber)

        verticalLayout.addLayout(horizontalLayoutOpts)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        verticalLayout.addWidget(buttonBox)

    def _fillChampComboBox(self):
        self._comboBoxChamp.addItems([v.value for v in list(ChampName)])

    def _fillDayNumberComboBox(self):
        self._comboBoxDayNumber.addItems([str(v) for v in range(1, 39)])

    def getSrcPath(self):
        return self._srcDesPathWidget.getSrcPath()

    def getDesPath(self):
        return self._srcDesPathWidget.getDesPath()

    def getChampName(self):
        return self._comboBoxChamp.currentText()

    def getDayNumber(self):
        return self._comboBoxDayNumber.currentText()


class NewLeagueDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(NewLeagueDialog, self).__init__(parent)
        self._nameLeagueEdit = None

        self.setupUi()

    def setupUi(self):
        verticalLayout = getConfiguredLayout(LayoutType.VERTICAL.value, parent=self)
        horizontalLayout = getConfiguredLayout(LayoutType.HORIZONTAL.value, margins=[0])

        label = QtWidgets.QLabel(self)
        label.setText("name : ")
        horizontalLayout.addWidget(label)

        self._nameLeagueEdit = QtWidgets.QLineEdit(self)
        horizontalLayout.addWidget(self._nameLeagueEdit)
        verticalLayout.addLayout(horizontalLayout)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
                                               parent=self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        verticalLayout.addWidget(buttonBox)

    def getLeagueName(self):
        return self._nameLeagueEdit.text()


class GetPathMercatoTurnDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(GetPathMercatoTurnDialog, self).__init__(parent)

        self._pathWidget = None

        self.setupUi()

    def setupUi(self):
        verticalLayout = getConfiguredLayout(LayoutType.VERTICAL.value, parent=self)
        self._pathWidget = FileBrowserPath("Src", self.tr("Files (*.csv)"), self)
        verticalLayout.addWidget(self._pathWidget)
