# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui
from enum import Enum


class MimeTypes(Enum):
    PLAYER = "Player"


class UserRoles(Enum):
    ID_ROLE = QtCore.Qt.UserRole + 1
