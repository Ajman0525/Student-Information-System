from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression

import re, csv, os


class AddStudent(QtWidgets.QDialog):
    student_added = QtCore.pyqtSignal(list)  
    student_edited = QtCore.pyqtSignal(list)

    def __init__(self, parent=None, student_data=None, table_model=None):
        super().__init__(parent if isinstance(parent, QWidget) else None) 
        self.table_model = table_model

        self.editing = student_data is not None
        self.original_id = student_data[0] if self.editing else ""

        self.setObjectName("Dialog")
        self.setWindowTitle("Student Information System")
        self.setWindowIcon(QIcon("Images/ChickIcon.png"))
        self.resize(311, 313)

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


        # Set Fonts
        #----------------------------------
        fixedsys_font = QtGui.QFont()
        fixedsys_font.setFamily("Fixedsys")

        terminal_font = QtGui.QFont()
        terminal_font.setFamily("Terminal")
        terminal_font.setPointSize(14)
        terminal_font.setBold(True)
        terminal_font.setWeight(75)

        # Title
        #------------------------------------------------------
        self.addStudent = QtWidgets.QLabel("ADD STUDENT", self)
        self.addStudent.setStyleSheet("color: #CD853F")
        self.addStudent.setGeometry(100, 20, 121, 21)
        self.addStudent.setFont(terminal_font)

        # ID Label
        #-------------------------------------------------
        self.idText = QtWidgets.QLabel("ID NUMBER:", self)
        self.idText.setGeometry(20, 60, 91, 20)
        self.idText.setFont(fixedsys_font)
        self.idNumber = QtWidgets.QLineEdit(self)
        self.idNumber.setGeometry(140, 60, 151, 20)
        self.idNumber.setFont(fixedsys_font)

        # First Name
        #-----------------------------------------------------
        self.fNameText = QtWidgets.QLabel("FIRST NAME:", self)
        self.fNameText.setGeometry(20, 90, 81, 16)
        self.fNameText.setFont(fixedsys_font)
        self.firstName = QtWidgets.QLineEdit(self)
        self.firstName.setGeometry(140, 90, 151, 20)
        self.firstName.setFont(fixedsys_font)

        # Last Name
        #-------------------------------------------------------
        self.lastNameText = QtWidgets.QLabel("LAST NAME:", self)
        self.lastNameText.setGeometry(20, 120, 81, 16)
        self.lastNameText.setFont(fixedsys_font)
        self.lastName = QtWidgets.QLineEdit(self)
        self.lastName.setGeometry(140, 120, 151, 20)
        self.lastName.setFont(fixedsys_font)

        # Year Level
        #---------------------------------------------------------
        self.yearLevelText = QtWidgets.QLabel("YEAR LEVEL:", self)
        self.yearLevelText.setGeometry(20, 150, 91, 16)
        self.yearLevelText.setFont(fixedsys_font)
        self.yearLevel = QtWidgets.QComboBox(self)
        self.yearLevel.setGeometry(140, 150, 111, 20)
        self.yearLevel.setFont(fixedsys_font)
        self.yearLevel.addItems(["1ST YEAR", "2ND YEAR", "3RD YEAR", "4TH YEAR"])

        # Gender
        #--------------------------------------------------
        self.genderText = QtWidgets.QLabel("GENDER:", self)
        self.genderText.setGeometry(20, 180, 61, 16)
        self.genderText.setFont(fixedsys_font)
        self.gender = QtWidgets.QLineEdit(self)
        self.gender.setGeometry(140, 180, 151, 20)
        self.gender.setFont(fixedsys_font)

        # Program
        #----------------------------------------------------------------
        self.studentProgramText = QtWidgets.QLabel("PROGRAM CODE:", self)
        self.studentProgramText.setGeometry(20, 210, 111, 16)
        self.studentProgramText.setFont(fixedsys_font)
        self.studentProgram = QtWidgets.QComboBox(self)
        self.load_program_codes()
        self.studentProgram.addItems(["UNENROLLED"])
        self.studentProgram.setGeometry(140, 210, 111, 20)
        self.studentProgram.setFont(fixedsys_font)
        
        
        # Edit Popup
        #---------------------------------------
        self.editing = student_data is not None
        if self.editing:
            self.addStudent.setText("EDIT STUDENT")
            self.addStudent.setGeometry(QtCore.QRect(90, 20, 131, 21))
            self.idNumber.setText(student_data[0])
            self.firstName.setText(student_data[1])
            self.lastName.setText(student_data[2])
            self.yearLevel.setCurrentText(student_data[3])
            self.gender.setText(student_data[4])
            self.studentProgram.setCurrentText(student_data[5])
            
            
        # Validators to allow number on inputs
        #----------------------------------------------------------------------------------------------------------------------
        text_validator = QRegularExpressionValidator(QRegularExpression(r"^[A-Za-z0-9](?:[A-Za-z0-9\s-]*[A-Za-z0-9])?$"), self) 
        self.firstName.setValidator(text_validator)
        self.lastName.setValidator(text_validator)
        
        #No Number on inputs
        #-------------------------------------------------------------------------------------------------------------
        text_validator = QRegularExpressionValidator(QRegularExpression(r"^[A-Za-z](?:[A-Za-z\s-]*[A-Za-z])?$"), self) 
        self.gender.setValidator(text_validator)

        #Validator to prevent incorrect input on ID Numbers
        #_-------------------------------------------------------------------------------------
        id_validator = QRegularExpressionValidator(QRegularExpression(r"^2\d{3}-\d{4}$"), self)  
        self.idNumber.setValidator(id_validator)

        # Confirmation Button
        #----------------------------------------------------------------------------------------------------------------------------
        self.confirmationButton = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        self.confirmationButton.setGeometry(130, 260, 156, 30)
        self.confirmationButton.setFont(fixedsys_font)
        self.confirmationButton.setObjectName("confirmationButton")
        self.confirmationButton.accepted.connect(self.accept_data)
        self.confirmationButton.rejected.connect(self.reject)
        

        # -------------------------------- #
        #       Student Data Manager       #
        # -------------------------------- #
    
    def accept_data(self):
        
        id_number = self.idNumber.text().strip()
        first_name = re.sub(r'\s+', ' ', self.firstName.text().strip())
        last_name = re.sub(r'\s+', ' ', self.lastName.text().strip())
        gender = re.sub(r'\s+', ' ', self.gender.text().strip())

        self.firstName.setText(first_name.title())
        self.lastName.setText(last_name.title())
        self.gender.setText(gender.capitalize())

        if not id_number or not first_name or not last_name or not gender:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out before submitting.")
            return
    
        if not re.match(r"^2\d{3}-\d{4}$", id_number):
            QMessageBox.warning(self, "Input Error", "ID Number must follow the format YYYY-XXXX (e.g., 2022-0525).")
            return
        
        invalid_fields = []

        gender_regex = r"^[A-Za-z]+(?:\s[A-Za-z]+)*(?:-[A-Za-z]+)?$" #Numbers are invalid                  
        name_regex = r"^[A-Za-z0-9]+(?:\s[A-Za-z0-9]+)*(?:-[A-Za-z0-9]+)?$" #Number on inputs are allowed
        
        if not re.match(name_regex, first_name):
            invalid_fields.append("First Name")

        if not re.match(name_regex, last_name):
            invalid_fields.append("Last Name")

        if not re.match(gender_regex, gender):
            invalid_fields.append("Gender")

        if invalid_fields:
            QMessageBox.warning(self, "Input Error", f"{', '.join(invalid_fields)} should be properly formatted.")
            return
        
        if self.is_duplicate_id(id_number):
            QMessageBox.warning(self, "Duplicate Error", f"\nID Number: {id_number} \nalready belongs to another student.")
            return
        
        student_data = self.get_data()

        if self.editing:
            self.student_edited.emit(student_data)

        else: 
            self.student_added.emit(student_data)

        self.accept()  

    def is_duplicate_id(self, id_number):
        if self.table_model:
            for row in range(self.table_model.rowCount()):
                item = self.table_model.item(row, 0)
                existing_id = item.text().strip() if item else ""
                
                if existing_id == id_number:
                    if self.editing and id_number == self.original_id:
                        continue  
                    
                    return True
        
        file_path = 'CSV Files/SSIS - STUDENT.csv'
        if os.path.exists(file_path):
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0].strip() == id_number:
                        if self.editing and id_number == self.original_id:
                            continue  
                        
                        return True
        
        return False
        
    def get_data(self):
        return [
            self.idNumber.text(),
            self.firstName.text(),
            self.lastName.text(),
            self.yearLevel.currentText(),
            self.gender.text(),
            self.studentProgram.currentText(),
        ]
    
    def load_program_codes(self):
        file_path = "CSV Files/SSIS - PROGRAM.csv"
        self.studentProgram.clear()  # Clear existing items

        if os.path.exists(file_path):
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row

                for row in reader:
                    if row:  
                        self.studentProgram.addItem(row[0])  # Add Program Code
