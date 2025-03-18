from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QHBoxLayout, QTableWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys, csv, copy

from Images import header_rc

from Buttons.addButton import AddButton
from Popups.AddStudent import AddStudent
from Popups.AddProgram import AddProgram
from Popups.AddCollege import AddCollege

from Buttons.removeButton import RemoveButton
from Buttons.updateButton import UpdateButton
from Buttons.editButton import EditButton
from SearchBar.searchTab import SearchBar

class Display(object):
    

    '''=========================================================='''
    '''|                    WINDOW DISPLAY                      |'''
    '''=========================================================='''
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(878, 564)
        MainWindow.setMinimumSize(QtCore.QSize(878, 600))
        MainWindow.setMaximumSize(QtCore.QSize(878, 600))
        MainWindow.setWindowIcon(QIcon("Images/ChickIcon.png"))
        MainWindow.setStyleSheet("background-color: #fce090")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(100, 18, 381, 41))
        font = QtGui.QFont()
        font.setFamily("Pixeboy")
        font.setPointSize(24)
        self.header.setFont(font)
        self.header.setObjectName("header")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 81, 61))
        self.label.setStyleSheet("background-image: url(:/newPrefix/Icons for SSIS/Untitled_design-removebg-preview.png);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/Icons for SSIS/Untitled_design-removebg-preview.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        

        # ADD BUTTON
        # ------------------------------------------------
        AddButton(self) 
        self.addButton.clicked.connect(self.show_add_entry) 

        # REMOVE BUTTON
        # ------------------------------------------------
        RemoveButton(self)
        self.removeButton.clicked.connect(self.removeData)

        # UPDATE BUTTON
        # ------------------------------------------------
        UpdateButton(self) 
        self.updateButton.clicked.connect(lambda: self.updateCsv(self.getActiveCsvFile()))
        self.updateButton.setVisible(False) 
        self.last_update_type = None

        # EDIT BUTTON
        # ------------------------------------------------
        EditButton(self)
        self.editButton.clicked.connect(self.edit_student)


        # -------------------------------- #
        #           SEARCH BAR             #
        # -------------------------------- #        
        self.searchTab = SearchBar(self.centralwidget)
        self.searchTab.setGeometry(QtCore.QRect(680, 52, 181, 25))
        self.searchTab.setObjectName("searchTab")
        self.searchTab.setStyleSheet("""background-color: white; 
                                        border: 3px solid peru; 
                                        border-radius: 9px; 
                                        padding: 2px;
                                        color: gray;
                                        font-family: "Fixedsys";
                                        font-size: 12px;""")
        self.searchTab.textChanged.connect(self.searchCsv)
        

                    
        # -------------------------------- #
        #           TABLE DISPLAY          #
        # -------------------------------- #     
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(25, 130, 825, 401))
        self.tableView.setObjectName("tableView")
        self.tableView.setStyleSheet("""
            background-color: white;
            border: 3px solid peru;                      
            selection-background-color: #ffcc80;  /* Change highlight color */    
            selection-color: white;  /* Change text color of selected row */                                              
                                                 
        """)
        self.model = QtGui.QStandardItemModel(MainWindow)
        self.tableView.setModel(self.model)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) #For table display automatic fitting
        
        #Focus and Selection of Rows    
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows) #Highlight the entire rows
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setFocusPolicy(Qt.NoFocus)
        self.tableView.selectionModel().selectionChanged.connect(self.highlight_selected_row) #Selected row is bolder in color
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        
        # -------------------------------- #
        #         SORTING COLUMNS          #
        # -------------------------------- #   
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)  # Case-insensitive sorting
        self.proxy_model.setSortRole(QtCore.Qt.DisplayRole)  # Sort by display text

        self.tableView.setModel(self.proxy_model)  # Apply proxy model to table
        self.tableView.setSortingEnabled(True)  # Enable sorting'''
        




        # -------------------------------- #
        #           TABS DISPLAY           #
        # -------------------------------- #  
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("""
            QTabBar {                                                                   
            font-family: Fixedsys;                          
            font: bold;                                                
            }

            /* Tabs */
            QTabBar::tab {
                color: #BEA67A;                    
                min-width: 100px;  /* Tab width */
                height: 15px;  /* Tab height */                                
                padding: 10px;
                border: 2px solid black; /* Dark Brown Border */
                border-radius: 10px;
                
            }

            /* Selected Tab */
            QTabBar::tab:selected {
                background: #CD853F; 
                color: #fce090;
               
            }

            /* Unselected Tabs */
            QTabBar::tab:!selected {
                width: 69px;
                                                       
            }                                                                                                          
        """)
        self.tabWidget.setGeometry(QtCore.QRect(25, 91, 825, 432))
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.studentTab = QtWidgets.QWidget()
        self.studentTab.setObjectName("studentTab")
        self.tabWidget.addTab(self.studentTab, "")
        self.programTab = QtWidgets.QWidget()
        self.programTab.setObjectName("programTab")
        self.tabWidget.addTab(self.programTab, "")
        self.collegeTab = QtWidgets.QWidget()
        self.collegeTab.setObjectName("collegeTab")
        self.tabWidget.addTab(self.collegeTab, "")
        self.tableView.raise_()
        
        
        # -------------------------------- #
        #       SEARCH BAR COMBO BOX       #
        # -------------------------------- #  
        self.searchComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.searchComboBox.setGeometry(QtCore.QRect(547, 52, 123, 25)) 
        self.searchComboBox.setObjectName("searchComboBox")
        self.searchComboBox.setStyleSheet("""
            QComboBox {
                background-color: white; 
                border: 3px solid peru; 
                padding: 2px;
                color: gray;
                font-family: "Fixedsys";                                                                                 
            }      

            /* Dropdown Styling */
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #ffcc80; /* Background color when selected */
                selection-color: white; /* Font color when selected */
                border: 1px solid peru;
            }

            QComboBox QAbstractItemView::item {
                color: black; 
            }

            QComboBox:on {
                color: peru;
            }
        """)
        #Default Combo Box Options
        self.searchComboBox.addItem("Search By:")
        self.searchComboBox.addItems(["Student ID", "First Name", "Last Name", "Year Level", "Gender", "Program Code"])
        

        #Invisible Features (not enabled in Qt Designer)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #CSV Display
        self.studentCsv() #Display Student Tab after running
        self.tabWidget.currentChanged.connect(self.displayTabs)



    '''=========================================================='''
    '''|                CSV FILE MANIPULATIONS                  |'''
    '''=========================================================='''

    # DELETING ROWS FROM TABS
    # ----------------------------------------------------------------
    def removeData(self):
        selected_tab = self.tabWidget.currentIndex()
        selected_rows = self.tableView.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(None, "Warning", "Please select a row")
            return

        # Custom Messages Based on Tab
        if selected_tab == 0:  # Student Tab
            title = "Delete Student"
            message = "\nAre you sure you want to delete the selected student?\nThis action cannot be undone!"
            icon = QMessageBox.Warning

        elif selected_tab == 1:  # Program Tab
            title = "Delete Program"
            message = "\nAre you sure you want to delete this program?\n It will affect all students enrolled in it."
            icon = QMessageBox.Critical

        elif selected_tab == 2:  # College Tab
            title = "Delete College"
            message = "\nAre you sure you want to delete this college?\nAll associated entries will be affected."
            icon = QMessageBox.Question


        # Create Unique QMessageBox
        confirm = QMessageBox()
        confirm.setWindowTitle(title)
        confirm.setText(message)
        confirm.setIcon(icon)
        confirm.setWindowIcon(QIcon("Images/ChickIcon.png"))  # Set custom icon
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        
        response = confirm.exec_()

        if response == QMessageBox.No:
            return

        # Proceed with deletion logic
        selected_rows.sort(reverse=True, key=lambda x: x.row())  # Avoid shifting issues

        for index in selected_rows:
            source_index = self.proxy_model.mapToSource(index)
            actual_row = source_index.row()
            row_data = [self.model.item(actual_row, col).text() if self.model.item(actual_row, col) else "" 
                        for col in range(self.model.columnCount())]

            self.model.removeRow(actual_row)

            if selected_tab == 2:  # College Tab
                self.cascade_delete_college(row_data[0])

            elif selected_tab == 1:  # Program Tab
                self.cascade_delete_program(row_data[0])

            elif selected_tab == 0:  # Student Tab
                student_id = row_data[0]
              
                
                file_name = "CSV Files/SSIS - STUDENT.csv"
                with open(file_name, "r", newline="", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    students = [row for row in reader if row[0] != student_id]
            
                with open(file_name, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(students)
            
                QMessageBox.information(None, "Success", "Student deleted successfully!")

    

    # SAVING CSV CHANGES
    # ----------------------------------------------------------------
    def updateCsv(self, file_name):
        
        if not file_name:
            return

        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write headers
            headers = [self.model.headerData(i, Qt.Horizontal) for i in range(self.model.columnCount())]
            writer.writerow(headers)

            # Write data from the PROXY model (sorted/filtered view)
            for row in range(self.proxy_model.rowCount()):
                row_data = []
                for col in range(self.model.columnCount()):
                    index = self.proxy_model.index(row, col)  # Get index from proxy
                    item = self.proxy_model.data(index, Qt.DisplayRole)
                    row_data.append(item if item else "")
                writer.writerow(row_data)

        if self.last_update_type == "Student":
            QMessageBox.information(None, "Success", "Student records have been updated successfully!")
        elif self.last_update_type == "Program":
            QMessageBox.information(None, "Success", "Program records have been updated successfully!")
        elif self.last_update_type == "College":
            QMessageBox.information(None, "Success", "College records have been updated successfully!")
        else:
            QMessageBox.information(None, "Success", "Changes saved successfully!")

        self.updateButton.setVisible(False)  # ✅ Hide update button after saving
        self.last_update_type = None  # ✅ Reset update type

        
    def getActiveCsvFile(self):
        if self.tabWidget.currentIndex() == 0:
            return "CSV Files/SSIS - STUDENT.csv"
        elif self.tabWidget.currentIndex() == 1:
            return "CSV Files/SSIS - PROGRAM.csv"
        elif self.tabWidget.currentIndex() == 2:
            return "CSV Files/SSIS - COLLEGE.csv"
        return None

                                                #########################################################
                                                #                     SEARCH BAR                        #
                                                #########################################################  
    def searchCsv(self):
        search_text = self.searchTab.text().strip().lower()  # Get the text from search bar
        selected_column = self.searchComboBox.currentText()
        

        if not search_text or selected_column == "Search By:":
            file_name = self.getActiveCsvFile()
            if file_name:
                self.displayCsv(file_name)
            return
        
        file_name = self.getActiveCsvFile()
        column_index = self.getColumnIndex(selected_column) 

        if column_index is None:
            return

        self.model.clear()
            
        try:
            with open(file_name, "r", encoding="utf-8") as fileInput:
                reader = csv.reader(fileInput)
                headers = next(reader, None)  # Read the header row
                if headers:
                    self.model.setHorizontalHeaderLabels(headers)

                for row in reader:
                    if len(row) > column_index:         
                        if search_text in row[column_index].lower():  # Case-insensitive search
                            items = [QtGui.QStandardItem(field) for field in row]
                            self.model.appendRow(items)  # Add matching rows
                    else:
                        print(f"Skipping row due to insufficient columns: {row}")
                        
        except FileNotFoundError:
            print(f"Error: {file_name} not found.")  # Handle missing file

    def updateComboBox(self, items):
        self.searchComboBox.clear()  
        for item in items:
            self.searchComboBox.addItem(item)
            
    #Column Search
    def getColumnIndex(self, column_name):
        headers = [self.model.headerData(i, Qt.Horizontal) for i in range(self.model.columnCount())]
        
        if not headers:
            print("Error: No headers found in the table.")
            return None

        headers_upper = [header.upper() for header in headers if header]
        column_name_upper = column_name.upper()

        if column_name_upper in headers_upper:
            return headers_upper.index(column_name_upper)
        else:
            print(f"Error: Column '{column_name}' not found in headers: {headers}")
            return None
            
                                                #########################################################
                                                #                  TAB TABLE DISPLAY                    #
                                                #########################################################  
   
   
    def displayTabs(self, index):
        


        self.model.clear()
        # 1.) STUDENT TAB
        # ---------------------------------------------
        if index == 0:  
            self.studentCsv() #Display correct csv
            self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)
            self.addButton.setText("Add Student")
            self.removeButton.setText("Remove Student")
            self.updateButton.setText("Update Student")
            self.editButton.setText("Edit Student")
            self.editButton.clicked.disconnect()  
            self.editButton.clicked.connect(self.edit_student)
            self.updateComboBox(["Search By:", "Student ID", "First Name", "Last Name", "Year Level", "Gender", "Program Code"]) #Updates the search bar combo box
            
        # 2.) PROGRAM TAB
        # ---------------------------------------------
        elif index == 1:  
            self.programCsv() #Display correct csv
            self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)
            self.addButton.setText("Add Program")
            self.removeButton.setText("Remove Program")
            self.updateButton.setText("Update Program")
            self.editButton.setText("Edit Program")
            self.editButton.clicked.disconnect()  
            self.editButton.clicked.connect(self.edit_program)
            self.updateComboBox(["Search By:", "Program Code", "Program Name", "College Code"]) #Updates the search bar combo box
            
        # 2.) COLLEGE TAB
        # ---------------------------------------------
        elif index == 2:  
            self.collegeCsv()#Display correct csv
            self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)
            self.addButton.setText("Add College")
            self.removeButton.setText("Remove College")
            self.updateButton.setText("Update College")
            self.editButton.setText("Edit College")
            self.editButton.clicked.disconnect()  
            self.editButton.clicked.connect(self.edit_college)
            self.updateComboBox(["Search By:", "College Code", "College Name"]) #Updates the search bar combo box        

    
        # -------------------------------- #
        #       ROW HIGHLIGHT STYLE        #
        # -------------------------------- # 
    def highlight_selected_row(self, selected, deselected):
        # Reset font for all rows first
        for row in range(self.model.rowCount()):
            for col in range(self.model.columnCount()):
                item = self.model.item(row, col)
                if item:
                    font = item.font()
                    font.setBold(False)  # Reset to normal
                    item.setFont(font)

        # Apply bold font to selected rows
        for index in selected.indexes():
            row = index.row()
            for col in range(self.model.columnCount()):
                item = self.model.item(row, col)
                if item:
                    font = item.font()
                    font.setBold(True)  # Make selected row bold
                    item.setFont(font)

    # -------------------------------- #
    #          DISPLAYING CSV          #
    # -------------------------------- # 
    def displayCsv(self, fileName):
        self.model.clear()  #Clear any possible preexisting table
        with open(fileName, "r", encoding="utf-8") as fileInput:
            reader = csv.reader(fileInput)
            headers = next(reader, None)  # Read the first row as headers
            if headers:
                self.model.setHorizontalHeaderLabels(headers)
            
            for row in reader:
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)

        #self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)

    def studentCsv(self, force_refresh=False):
        self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)
        self.displayCsv("CSV Files/SSIS - STUDENT.csv")
       

    def programCsv(self):
        self.displayCsv('CSV Files/SSIS - PROGRAM.csv')

    def collegeCsv(self):
        self.displayCsv('CSV Files/SSIS - COLLEGE.csv')
    
    '''======================================================================='''
    '''|                                                                     |'''       
    '''|    SETTING DESIGN FOR BUTTONS, WINDOW TITLE, AND SEARCH COMBO BOX   |'''
    '''|                                                                     |'''
    '''======================================================================='''

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Student Information System"))
        self.addButton.setText(_translate("MainWindow", "Add Student"))
        self.removeButton.setText(_translate("MainWindow", "Remove Student"))
        self.updateButton.setText(_translate("MainWindow", "Update Student"))
        self.editButton.setText(_translate("MainWindow", "Edit Student"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.studentTab), _translate("MainWindow", "Student"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.programTab), _translate("MainWindow", "Program"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.collegeTab), _translate("MainWindow", "College"))
        self.header.setText(_translate("MainWindow", "STUDENT INFORMATION SYSTEM"))
        self.header.setStyleSheet("""color: peru
                                  """)
        button_style = """
        QPushButton {
            background-color: white;  /* White background */
            color: #4C4A4D;               /* Black Font */
            border: 1px solid #978C76;  /* Darker border */
            border-radius: 9px;         /* Rounded corners */
            padding: 5px;               /* Padding inside button */
        }
        QPushButton:hover {
            background-color: #c1c8d4;  /* When hovered */
        }
        QPushButton:pressed {
            background-color: #969ba3;  /* Darker gray when clicked */
        }
        """

        # Apply the style to all buttons
        self.addButton.setStyleSheet(button_style)
        self.removeButton.setStyleSheet(button_style)
        self.updateButton.setStyleSheet(button_style)
        self.editButton.setStyleSheet(button_style)


                                                        #########################################################
                                                        #                   MODIFYNG ENTRIES                    #
                                                        ######################################################### 

    '''=========================================================='''
    '''|                   EDITING ENTRIES                      |'''
    '''=========================================================='''
  
    # EDITING STUDENT TAB
    #---------------------------
    def edit_student(self):
        selected_index = self.tableView.selectionModel().currentIndex()  # Get the selected index
        if not selected_index.isValid():
            QMessageBox.warning(None, "Selection Error", "Please select a Student to edit.")
            return

        source_index = self.proxy_model.mapToSource(selected_index)
        selected_row = source_index.row()  # Get the row number

        student_data = [
            self.model.item(selected_row, col).text() if self.model.item(selected_row, col) else ""
            for col in range(self.model.columnCount())
        ]

        edit_dialog = AddStudent(self.centralwidget, student_data, table_model = self.model)
        if edit_dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_data = edit_dialog.get_data()
            self.apply_student_edits(selected_row, updated_data)
      



    # EDITING PROGRAM TAB
    #---------------------------
    def edit_program(self):
        selected_index = self.tableView.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(None, "Selection Error", "Please select a Program to edit.")
            return
     
        source_index = self.proxy_model.mapToSource(selected_index)
        selected_row = source_index.row()  

        program_data = [
            self.model.item(selected_row, col).text() if self.model.item(selected_row, col) else ""
            for col in range(self.model.columnCount())
        ]

        edit_dialog = AddProgram(self.centralwidget, program_data, table_model = self.model)
        if edit_dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_data = edit_dialog.get_data()

            self.apply_program_edits(selected_index.row(), updated_data)
     

    # EDITING COLLEGE TAB
    #---------------------------
    def edit_college(self):
        selected_index = self.tableView.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(None, "Selection Error", "Please select a College to edit.")
            return

        # Convert proxy index to source index
        source_index = self.proxy_model.mapToSource(selected_index)
        selected_row = source_index.row()


        # Get data from the source model, NOT the proxy model
        college_data = [
            self.model.item(selected_row, col).text() if self.model.item(selected_row, col) else ""
            for col in range(self.model.columnCount())
        ]

  

        edit_dialog = AddCollege(self.centralwidget, college_data, table_model=self.model)
        if edit_dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_data = edit_dialog.get_data()

            #Prevent the College tab from resetting the table after editing
            self.is_editing = True

            #Pass the correct source row
            self.apply_college_edits(selected_row, updated_data)






        
    '''=========================================================='''
    '''|          STORING CHANGES TO TEMPORARY STORAGE          |'''
    '''=========================================================='''

    #Stores the edit into a copy of CSV File for it to be saved manually later
    def apply_student_edits(self, row, updated_data):
        """ Updates the selected row in the table without saving to CSV immediately """
        if not updated_data:
            QMessageBox.warning(None, "Error", "No data provided.")
            return

        for col, value in enumerate(updated_data):
            item = QtGui.QStandardItem(value)
            self.model.setItem(row, col, item)

        #proxy_model.sort(0, QtCore.Qt.AscendingOrder)
        self.last_update_type = "Student"
        self.updateButton.setVisible(True)

        QMessageBox.information(None, "Success", "Changes applied! Click 'Update' to save them permanently.")
    
    #Stores the edit into a copy of  CSV File for it to  be saved manually later
    
    def apply_program_edits(self, proxy_row, updated_data):
        if not updated_data:
            QMessageBox.warning(None, "Error", "No data provided.")
            return

        # Convert proxy row to source row
        source_index = self.proxy_model.mapToSource(self.proxy_model.index(proxy_row, 0))
        row = source_index.row()

        old_program_code_item = self.model.item(row, 0)
        if old_program_code_item is None or old_program_code_item.text().strip() == "":
            QMessageBox.warning(None, "Error", "No valid Program Code found.")
            return

        old_program_code = old_program_code_item.text().strip()
        new_program_code = updated_data[0].strip()

        # Update UI Table Model (Program Tab)
        for col, value in enumerate(updated_data):
            item = QtGui.QStandardItem(value)
            self.model.setItem(row, col, item)

        # Update related students
        if old_program_code != new_program_code:
            self.update_student_program_code(old_program_code, new_program_code)

        # Save changes immediately
        self.updateCsv("CSV Files/SSIS - PROGRAM.csv")

        QMessageBox.information(None, "Success", "Program Code updated and saved automatically!")

    def apply_college_edits(self, row, updated_data):
        if not updated_data:
            QMessageBox.warning(None, "Error", "No data provided.")
            return

        old_college_code_item = self.model.item(row, 0)
        if old_college_code_item is None or old_college_code_item.text().strip() == "":
            QMessageBox.warning(None, "Error", "No valid College Code found.")
            return

        old_college_code = old_college_code_item.text().strip()
        new_college_code = updated_data[0].strip()

        #  Update UI Table Model (College Tab)
        for col, value in enumerate(updated_data):
            item = self.model.item(row, col)
            if item:
                item.setData(value, QtCore.Qt.DisplayRole)
            else:
                self.model.setItem(row, col, QtGui.QStandardItem(value))

        # Update related programs if College Code changed
        if old_college_code != new_college_code:
            self.update_program_college_code(old_college_code, new_college_code)

        #  Save changes immediately
        self.updateCsv("CSV Files/SSIS - COLLEGE.csv")

        QMessageBox.information(None, "Success", "College Code updated and saved automatically!")


    '''=========================================================='''
    '''|                  CASCADING EFFECT                      |'''
    '''=========================================================='''
    
    def update_program_college_code(self, old_college_code, new_college_code):
        file_path = "CSV Files/SSIS - PROGRAM.csv"
        programs = []

        #  Load program data
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            programs = [row for row in reader]

        #  Update college code in programs
        updated = False
        for row in programs:
            if row[2] == old_college_code:
                row[2] = new_college_code
                updated = True

        #  Save changes ONLY if updates were made
        if updated:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(programs)

            # Force UI Refresh for Program Tab
            if self.tabWidget.currentIndex() == 1:
                self.programCsv()

    def update_student_program_code(self, old_program_code, new_program_code):
        file_path = "CSV Files/SSIS - STUDENT.csv"
        students = []
        updated = False 

        #  Load student data
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            students = [row for row in reader]

  
        for row in students:
           
            if len(row) > 5 and row[5] == old_program_code:  # Column 5 = Program Code
                row[5] = new_program_code  # Update Program Code
                updated = True

        #  Save changes only if updates were made
        if updated:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(students)  

            # ✅ Only refresh Student Tab **if the user is already there**
            if self.tabWidget.currentIndex() == 0:
                self.studentCsv()  #  Refresh Student Table only when user is in Student Tab


    def cascade_delete_college(self, college_code):
        college_file = "CSV Files/SSIS - COLLEGE.csv"
        program_file = "CSV Files/SSIS - PROGRAM.csv"
        student_file = "CSV Files/SSIS - STUDENT.csv"

        # Remove the College from CSV
        with open(college_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            colleges = [row for row in reader if row[0] != college_code]  # Keep only colleges NOT matching the deleted one

        with open(college_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(colleges)

        #  Remove Programs under the College
        with open(program_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            programs = [row for row in reader if row[2] != college_code]  # Filter out programs under deleted college

        with open(program_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(programs)

        #  Update Students (Mark as UNENROLLED if their Program was deleted)
        with open(student_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            students = []
            deleted_programs = {p[0] for p in programs}  # Get remaining program codes
            for row in reader:
                if row[5] not in deleted_programs:  
                    row[5] = "UNENROLLED"  # If student's program was deleted, mark as UNENROLLED
                students.append(row)

        with open(student_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(students)

        # Refresh UI
        self.collegeCsv()
        self.programCsv()
        self.studentCsv()

        self.displayTabs(self.tabWidget.currentIndex())
        QMessageBox.information(None, "Success", "College deleted and associated entries updated successfully!")

    def cascade_delete_program(self, program_code):
        program_file = "CSV Files/SSIS - PROGRAM.csv"
        student_file = "CSV Files/SSIS - STUDENT.csv"

        #  Remove the Program from CSV
        with open(program_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            programs = [row for row in reader if row[0] != program_code]  # Keep programs that are NOT being deleted

        with open(program_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(programs)

        # Update Students (Mark as UNENROLLED if their Program was deleted)
        with open(student_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            students = []
            remaining_programs = {p[0] for p in programs}  # Get remaining program codes
            for row in reader:
                if row[5] not in remaining_programs:  
                    row[5] = "UNENROLLED"  # If student's program was deleted, mark as UNENROLLED
                students.append(row)

        with open(student_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(students)

        # Refresh UI
        self.programCsv()
        self.studentCsv()

        self.displayTabs(self.tabWidget.currentIndex())
        QMessageBox.information(None, "Success", "Program deleted and students updated successfully!")

    '''=========================================================='''
    '''|                   UPDATING RECORD                      |'''
    '''=========================================================='''

    # UPDATING STUDENT
    #-----------------------------------------------
    def update_student_record(self, updated_student):
        file_path = "CSV Files/SSIS - STUDENT.csv"
        students = []

        # Read all students
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            students = [row for row in reader]

        # Update the student with the matching ID
        for i, student in enumerate(students):
            if student[0] == updated_student[0]:  # Match ID number
                students[i] = updated_student
                break

        # Save the updated list
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(students)

        QMessageBox.information(None, "Success", "Student added successfully! Click 'Update' to save changes.")
        
        self.studentCsv()
    
    # UPDATING PROGRAM
    #-----------------------------------------------
    def update_program_record(self, updated_program):
        file_path = "CSV Files/SSIS - PROGRAM.csv"
        programs = []

        # Read all programs
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            programs = [row for row in reader]

        # Update the program with the matching program code
        for i, program in enumerate(programs):
            if program[0] == updated_program[0]:  # Match program code
                programs[i] = updated_program
                break

        # Save the updated list
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(programs)

        QMessageBox.information(None, "Success", "Program added successfully! Click 'Update' to save changes.")
        
        self.programCsv()

    # UPDATING COLLEGE
    #-----------------------------------------------
    def update_college_record(self, updated_college):
        file_path = "CSV Files/SSIS - COLLEGE.csv"
        colleges = []

        # Read all programs
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            colleges = [row for row in reader]

        # Update the program with the matching program code
        for i, college in enumerate(colleges):
            if college[0] == updated_college[0]:  # Match program code
                colleges[i] = updated_college
                break

        # Save the updated list
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(colleges)

        QMessageBox.information(None, "Success", "College added successfully! Click 'Update' to save changes.")
        
        self.collegeCsv()

    '''=========================================================='''
    '''|                    ADDING ENTRY                        |'''
    '''=========================================================='''
    
    # ADDING STUDENT
    #-------------------------------------
    def add_student_to_csv(self, new_data):
        if not new_data:
            QMessageBox.warning(None, "Error", "No data provided.")
            return

        try:
            items = [QtGui.QStandardItem(field) for field in new_data]
            self.model.appendRow(items)  

            self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)


            self.last_update_type = "Student"
            self.updateButton.setVisible(True)

            QMessageBox.information(None, "Success", "Student added successfully! Click 'Update' to save changes.")

            self.updateButton.setVisible(True)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to add student:\n{str(e)}")   

    # ADDING PROGRAM
    #-------------------------------------
    def add_program_to_csv(self, new_data):
        if not new_data:
            QMessageBox.warning(None, "Error", "No data provided.")

        try:
            items = [QtGui.QStandardItem(field) for field in new_data]
            self.model.appendRow(items)  
             

            self.last_update_type = "Program"
            self.updateButton.setVisible(True)

            QMessageBox.information(None, "Success", "Program added successfully! Click 'Update' to save changes.")

            
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to add program:\n{str(e)}")

    def update_student_program_combobox(self, program_code):
        for i in range(self.studentProgram.count()):
            if self.studentProgram.itemText(i) == program_code:
                return  # Already exists

        self.studentProgram.addItem(program_code)

    # ADDING COLLEGE
    #-------------------------------------  
    def add_college_to_csv(self, new_data):
        if not new_data:
            QMessageBox.warning(None, "Error", "No data provided.")

        try:
            items = [QtGui.QStandardItem(field) for field in new_data]
            self.model.appendRow(items)  

            self.last_update_type = "College"
            self.updateButton.setVisible(True)

            QMessageBox.information(None, "Success", "College added successfully! Click 'Update' to save changes.")

            
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to add college:\n{str(e)}")

    def update_college_code_combobox(self, college_code):
        for i in range(self.collegeCode.count()):
            if self.collegeCode.itemText(i) == college_code:
                return  # Already exists

        self.collegeCode.addItem(college_code)


    '''=========================================================='''
    '''|                     POPUP WINDOWS                      |'''
    '''=========================================================='''
    def show_add_entry(self):
        current_tab = self.tabWidget.currentIndex()

        if current_tab == 0:
            dialog = AddStudent(parent=self, student_data=None, table_model=self.model)
            
        elif current_tab == 1:
            dialog = AddProgram(parent=self, program_data=None, table_model=self.model)
            
        elif current_tab == 2:
            dialog = AddCollege(parent=self, college_data=None, table_model=self.model)
        
        else:
            return
        
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_data = dialog.get_data()
            if current_tab == 0:
                self.add_student_to_csv(new_data)
            elif current_tab == 1:
                self.add_program_to_csv(new_data)
            elif current_tab == 2:
                self.add_college_to_csv(new_data)
