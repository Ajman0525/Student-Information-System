from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression

import re, csv, os

class AddCollege(QtWidgets.QDialog):
    college_added = QtCore.pyqtSignal(list)
    college_edited = QtCore.pyqtSignal(list)
    
    def __init__(self, parent = None, college_data = None, table_model = None):
        super().__init__(parent if isinstance(parent, QWidget) else None)
        self.table_model = table_model
        self.college_data = college_data
        self.editing = college_data is not None

        self.original_code = college_data[0].strip().lower() if self.editing else None

        self.setObjectName("Dialog")
        self.setWindowTitle("Student Information System")
        self.resize(412, 229)
        self.setWindowIcon(QIcon("Images/ChickIcon.png"))
        
        self.setStyleSheet("""
            QDialog {
                background-color: #fce090; 
            }  
                                                    
            QLineEdit {
                font-family: 'Fixedsys';
                color: black; 
                background-color: white; 
                border: 1px solid #5D6D7E; /* Border color */
                border-radius: 5px;
                
            }

            QComboBox {
                font-family: 'Fixedsys';
                color: black;
                background-color: white;
                border: 1px solid #5D6D7E;
                border-radius: 5px;
            }
                           

            QPushButton {
                font-family: 'Fixedsys';
                background-color: white; 
                color: black;
                border-radius: 5px;
                padding: 20px
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

        #Set Fonts
        #----------------------------------
        fixedsys_font = QtGui.QFont()
        fixedsys_font.setFamily("Fixedsys")

        terminal_font = QtGui.QFont()
        terminal_font.setFamily("Terminal")
        terminal_font.setPointSize(14)
        terminal_font.setBold(True)
        terminal_font.setItalic(False)
        terminal_font.setWeight(75)

        #Title
        #------------------------------------------------------
        self.addCollege = QtWidgets.QLabel("ADD COLLEGE", self)
        self.addCollege.setStyleSheet("color: #CD853F")
        self.addCollege.setGeometry(140, 20, 121, 18)
        self.addCollege.setFont(terminal_font)
        

        #Container for Widgets
        #--------------------------------------------------
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 60, 371, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        
        #College Code
        #----------------------------------------------------------------------------------
        self.collegeCodeText = QtWidgets.QLabel("COLLEGE CODE:", self.verticalLayoutWidget)
        self.collegeCodeText.setFont(fixedsys_font)
        self.collegeCodeText.setObjectName("collegeCodeText")
        self.verticalLayout.addWidget(self.collegeCodeText)
       
        self.collegeCode = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.collegeCode.setFont(fixedsys_font)
        self.collegeCode.setObjectName("collegeCode")
        self.verticalLayout.addWidget(self.collegeCode)


        #College Name
        #----------------------------------------------------------------------------------
        self.collegeNameText = QtWidgets.QLabel("COLLEGE NAME:", self.verticalLayoutWidget)
        self.collegeNameText.setFont(fixedsys_font)
        self.collegeNameText.setObjectName("collegeNameText")
        self.verticalLayout.addWidget(self.collegeNameText)

        self.collegeName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.collegeName.setFont(fixedsys_font)
        self.collegeName.setObjectName("collegeName")
        self.verticalLayout.addWidget(self.collegeName)
        
        
        # Edit Popup
        #---------------------------------------
        self.editing = college_data is not None
        if self.editing:
            self.addCollege.setText("EDIT COLLEGE")
            self.addCollege.setGeometry(QtCore.QRect(140, 20, 131, 18))
            self.collegeCode.setText(college_data[0])
            self.collegeName.setText(college_data[1])

        #Validator
        #-------------------------------------------------------------------------------------------------------------
        text_validator = QRegularExpressionValidator(QRegularExpression(r"^[A-Za-z](?:[A-Za-z\s-]*[A-Za-z])?$"), self)
        self.collegeCode.setValidator(text_validator)
        self.collegeName.setValidator(text_validator)

        #Confirmation Buttons
        #----------------------------------------------------------------------------------------------------------------------------
        self.confirmationButton = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        self.confirmationButton.setGeometry(230, 180, 156, 30)
        self.confirmationButton.setFont(fixedsys_font)
        self.confirmationButton.setObjectName("confirmationButton")
        self.confirmationButton.accepted.connect(self.accept_data)
        self.confirmationButton.rejected.connect(self.reject)



        # -------------------------------- #
        #       College Data Manager       #
        # -------------------------------- #

    def accept_data(self):
        college_code = re.sub(r'\s+', ' ', self.collegeCode.text().strip()).upper()
        college_name = re.sub(r'\s+', ' ', self.collegeName.text().strip())

        self.collegeCode.setText(college_code)
        self.collegeName.setText(college_name)

        if not college_code or not college_name:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out before submitting.")
            return

        invalid_fields = []
        text_regex = r"^[A-Za-z]+(?:\s[A-Za-z]+)*(?:-[A-Za-z]+)?$"  # No numbers allowed

        if not re.match(text_regex, college_code):
            invalid_fields.append("College Code")

        if not re.match(text_regex, college_name):
            invalid_fields.append("College Name")


        if invalid_fields:
            QMessageBox.warning(self, "Input Error", f"{', '.join(invalid_fields)} should be properly formatted.")
            return

        if self.is_duplicate_college(college_code):
            QMessageBox.warning(self, "Duplicate Error", f"\nCollege Code: {college_code.upper()} already exists.")
            return

        college_data = self.get_data()

        if self.editing:
            self.college_edited.emit(college_data)
        else:
            self.college_added.emit(college_data)

        self.accept()

    def is_duplicate_college(self, college_code):
        college_code_lower =  college_code.strip().lower()
        

        if self.editing and college_code_lower == self.original_code:
            return False
        
        seen_codes = set()

        # 🚀 Check for duplicate in the table model (QStandardItemModel)
        if self.table_model:
            for row in range(self.table_model.rowCount()):
                item = self.table_model.item(row, 0)  # Assuming ID is in column 0
                if item: 
                    existing_code = item.text().strip().lower()
                    
                    if self.editing and existing_code == self.original_code:
                        continue

                    if existing_code == college_code_lower:
                        return True

        # 📂 Check for duplicate in the CSV file
        file_path = 'CSV Files/SSIS - COLLEGE.csv'
        if os.path.exists(file_path):
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row: #and row[0].strip().lower() == college_code_lower:  # Check first column (ID)
                        existing_code = row[0].strip().lower
                    if self.editing and existing_code == self.original_code:
                        continue
                    if existing_code == college_code_lower:
                        return True
                    
                    seen_codes.add(existing_code)
                    

        return False  

    def get_data(self):
        return [
            self.collegeCode.text(),
            self.collegeName.text(),
        ]


