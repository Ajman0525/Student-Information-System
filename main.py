#####################################################################################
#                          STUDENT INFORMATION SYSTEM                               #                 
#                                                                                   #
#  Made by: Ajman L. Mocsana                                                        #
#  Date:  From January 28, 2025 to February 28, 2025                                #
#####################################################################################


import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from UI.display import Display

def main():
    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Display()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


