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

    app.setStyleSheet("""
        QMessageBox {
            background-color: #fce090; 
            color: white;  
            font-family: "Fixedsys"; 
        }

        QPushButton {
                font-family: 'Fixedsys';
                background-color: white; 
                color: black;
                border-radius: 5px;
                padding: 10px
            }

            QPushButton:hover {
                background-color: #ffb36b; 
                color: white;
            }

            QPushButton:pressed {
                background-color: #CD853F; 
                color: white;
            }
    """)

    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


