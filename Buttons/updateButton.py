from PyQt5 import QtWidgets, QtGui, QtCore

def UpdateButton(parent):
    parent.updateButton = QtWidgets.QPushButton(parent.centralwidget)
    parent.updateButton.setGeometry(QtCore.QRect(445, 540, 135, 30))
    font = QtGui.QFont()
    font.setFamily("Fixedsys")
    parent.updateButton.setFont(font)
    parent.updateButton.setObjectName("updateButton")