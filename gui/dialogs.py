# coding=utf-8

import os
from core.defines import ChampName
from PySide2 import QtWidgets


class SrcDesPathWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(SrcDesPathWidget, self).__init__(parent)

        self._srcPathEdit = None
        self._desPathEdit = None

        self.setupUi()

    def setupUi(self):
        verticalLayout = QtWidgets.QVBoxLayout(self)

        horizontalLayoutSrc = QtWidgets.QHBoxLayout()
        labelSrc = QtWidgets.QLabel(self)
        labelSrc.setText("Src")
        horizontalLayoutSrc.addWidget(labelSrc)

        self._srcPathEdit = QtWidgets.QLineEdit(self)
        horizontalLayoutSrc.addWidget(self._srcPathEdit)

        srcBrowseButton = QtWidgets.QPushButton(self)
        srcBrowseButton.setText("Browse")
        srcBrowseButton.clicked.connect(self._changeSrcPath)
        horizontalLayoutSrc.addWidget(srcBrowseButton)

        horizontalLayoutDes = QtWidgets.QHBoxLayout()
        labelDes = QtWidgets.QLabel(self)
        labelDes.setText("Des")
        horizontalLayoutDes.addWidget(labelDes)

        self._desPathEdit = QtWidgets.QLineEdit(self)
        horizontalLayoutDes.addWidget(self._desPathEdit)

        desBrowseButton = QtWidgets.QPushButton(self)
        desBrowseButton.setText("Browse")
        desBrowseButton.clicked.connect(self._changeDesPath)
        horizontalLayoutDes.addWidget(desBrowseButton)

        verticalLayout.addLayout(horizontalLayoutSrc)
        verticalLayout.addLayout(horizontalLayoutDes)

    def _changeSrcPath(self):
        srcPath = QtWidgets.QFileDialog().getOpenFileName(self, self.tr("Select file"),
                                                          os.path.dirname(self._srcPathEdit.text()),
                                                          self.tr("Files (*.csv)"))[0]
        if srcPath != "":
            self._srcPathEdit.setText(srcPath)
            self._desPathEdit.setText(os.path.dirname(srcPath))

    def _changeDesPath(self):
        desPath = QtWidgets.QFileDialog().getExistingDirectory(self, self.tr("Select file"), self._desPathEdit.text())
        if len(desPath) != 0:
            self._desPathEdit.setText(desPath)

    def getSrcPath(self):
        return self._srcPathEdit.text()

    def getDesPath(self):
        return self._desPathEdit.text()


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
        verticalLayout = QtWidgets.QVBoxLayout(self)

        self._srcDesPathWidget = SrcDesPathWidget(self)
        verticalLayout.addWidget(self._srcDesPathWidget)

        horizontalLayoutOpts = QtWidgets.QHBoxLayout()
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
        self._comboBoxChamp.addItems([v.value for _, v in ChampName.items()])

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
        verticalLayout = QtWidgets.QVBoxLayout(self)
        horizontalLayout = QtWidgets.QHBoxLayout()

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
