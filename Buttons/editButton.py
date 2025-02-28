from PyQt5 import QtWidgets, QtCore, QtGui

def EditButton(parent):
    parent.editButton = QtWidgets.QPushButton(parent.centralwidget)
    parent.editButton.setGeometry(QtCore.QRect(25, 540, 120, 30))
    font = QtGui.QFont()
    font.setFamily("Fixedsys")
    parent.editButton.setFont(font)
    parent.editButton.setObjectName("editButton")
