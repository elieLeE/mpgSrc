# coding=utf-8

import os
from PySide2 import QtWidgets, QtCore
from gui.defines import LayoutType


def getConfiguredLayout(layoutType, margins=None, spacing=5, parent=None):
    def _getMarginFromTuple(tupleMargins):
        if len(tupleMargins) == 1:
            baseMargin = tupleMargins[0]
            tupleMargins = (baseMargin, baseMargin, baseMargin, baseMargin)
        elif len(tupleMargins) != 4:
            raise Exception("margins argument is not right : {}. If pass tuple, it has to have 1 or 4 values.".format(margins))
        return tupleMargins

    if margins is None:
        margins = (11, 11, 11, 11)
    elif isinstance(margins, list):
            margins = _getMarginFromTuple(tuple(margins))
    elif isinstance(margins, tuple):
        margins = _getMarginFromTuple(margins)

    layoutInst = None
    if layoutType == LayoutType.HORIZONTAL.value:
        layoutInst = QtWidgets.QHBoxLayout(parent)
    elif layoutType == LayoutType.VERTICAL.value:
        layoutInst = QtWidgets.QVBoxLayout(parent)

    if layoutInst is None:
        raise Exception("Type passed '{}' is unknown. Creation of the layout is not done.".format(layoutType))

    layoutInst.setSpacing(spacing)
    layoutInst.setContentsMargins(*margins)

    return layoutInst


class BrowserPath(QtWidgets.QWidget):
    pathChanged = QtCore.Signal(str)

    def __init__(self, pathName, pathAccepted, parent):
        super(BrowserPath, self).__init__(parent)

        self._pathName = pathName
        self._pathAccepted = pathAccepted
        self._pathEdit = None

        self.setupUi()

    def setupUi(self):
        horizontalLayoutSrc = getConfiguredLayout(LayoutType.HORIZONTAL.value, [0], 5, parent=self)

        if self._pathName != "":
            labelSrc = QtWidgets.QLabel(self)
            labelSrc.setText(self._pathName)
            horizontalLayoutSrc.addWidget(labelSrc)

        self._pathEdit = QtWidgets.QLineEdit(self)
        horizontalLayoutSrc.addWidget(self._pathEdit)

        srcBrowseButton = QtWidgets.QPushButton(self)
        srcBrowseButton.setText("Browse")
        srcBrowseButton.clicked.connect(self._changePath)
        horizontalLayoutSrc.addWidget(srcBrowseButton)

    def _getNewPath(self):
        raise NotImplementedError

    def _changePath(self):
        srcPath = self._getNewPath()
        if srcPath != "":
            self._pathEdit.setText(srcPath)
            self.pathChanged.emit(srcPath)

    def getPathChosen(self):
        return self._pathEdit.text()

    def resetPath(self, newPath):
        self._pathEdit.setText(newPath)


class FileBrowserPath(BrowserPath):
    def __init__(self, pathName, pathAccepted, parent):
        super(FileBrowserPath, self).__init__(pathName, pathAccepted, parent)

    def _getNewPath(self):
        return QtWidgets.QFileDialog().getOpenFileName(self, self.tr("Select file"),
                                                       os.path.dirname(self._pathEdit.text()),
                                                       self._pathAccepted)[0]


class DirectoryBrowserPath(BrowserPath):
    def __init__(self, pathName, pathAccepted, parent):
        super(DirectoryBrowserPath, self).__init__(pathName, pathAccepted, parent)

    def _getNewPath(self):
        return QtWidgets.QFileDialog().getExistingDirectory(self, self.tr("Select directory"), self._pathEdit.text())
