from PyQt5 import QtWidgets, QtCore, QtGui

def RemoveButton(parent):
    parent.removeButton = QtWidgets.QPushButton(parent.centralwidget)
    parent.removeButton.setGeometry(QtCore.QRect(709, 540, 141, 30))
    font = QtGui.QFont()
    font.setFamily("Fixedsys")
    parent.removeButton.setFont(font)
    parent.removeButton.setObjectName("removeButton")
