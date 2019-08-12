# coding=utf-8

from PySide2 import QtWidgets


def testQApp():
    app = QtWidgets.QApplication([])

    w = QtWidgets.QWidget()
    w.show()

    a = QtWidgets.QFileDialog.getOpenFileName(w)

    app.exec_()


def testEnum():
    from enum import Enum
    class DataBaseTreeViewColumn(Enum):
        NAME = 1, "Name"
        POSITION = 2, "Poste"
        TEAM = 3, "Equipe"
        EVAL_MOY = 4, "Note Moy"
        GAOL_NUMBER = 5, "Buts"
        PRIZE = 6, "Cote"
        PERCENT_TIT = 7, "Titulaire"

    print(list(DataBaseTreeViewColumn))


def testRange():
    l = list(range(10, 41, 10))

    l = list(arange(4, 10, 0.5))
    print(l)


def testRegex():
    import re
    base = "diego"
    testStr = "Lass"
    print(re.search(base, testStr, re.IGNORECASE) is not None)


def main():
    testRegex()


if __name__ == "__main__":
    main()
