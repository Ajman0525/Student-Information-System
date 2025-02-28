from PyQt5 import QtWidgets, QtCore, QtGui

def AddButton(parent):
    parent.addButton = QtWidgets.QPushButton(parent.centralwidget)
    parent.addButton.setGeometry(QtCore.QRect(584, 540, 121, 30))
    font = QtGui.QFont()
    font.setFamily("Fixedsys")
    parent.addButton.setFont(font)
    parent.addButton.setObjectName("addButton")
