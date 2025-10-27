# Student Information System (CSV File-Based)

A simple **Student Information System (SIS)** built using **PyQt5** and **Qt Designer**.  
This application allows users to manage student, program, and college information, with all data stored in **CSV files**.

---

## 📋 Features

- Add, edit, and delete student records  
- Manage college and program information  
- Detect duplicate student IDs  
- Store data persistently in CSV files  
- Intuitive GUI built with PyQt5 and Qt Designer  
- Automatically updates table views after changes  

---

## 🧰 Requirements

- Python 3.8 or higher  
- PyQt5  
- Pandas (optional, for CSV operations)

---

## ⚙️ Setup (Using Virtual Environment)

1. **Create a virtual environment**  
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install pyqt5 pandas
   ```

---

## 🚀 How to Run

1. Make sure your virtual environment is activated.  
2. Run the main application file:
   ```bash
   python main.py
   ```
3. The Student Information System window will open — you can now add, edit, or delete records.

---

## 📂 Project Structure

```
StudentInformationSystem/
├── Buttons/
│   ├── __init__.py     
│   ├── addButton.py
│   ├── editButton.py
│   ├── removeButton.py
│   └── updateButton.py
├── CSV Files/
│   ├── SSIS - COLLEGE.csv
│   ├── SSIS - PROGRAM.csv
│   └── SSIS - STUDENT.csv
├── Images/
│   ├── ChickIcon.png
│   ├── header_rc.py
│   └── headerpic.qrc
├── Popups/
│   ├── AddStudent.py
│   ├── AddProgram.py
│   └── AddCollege.py
├── SearchBar/
│   ├── __init__.py
│   └── searchTab.py
├── UI/
│   └── display.ui
├── main.py
├── venv/
└── README.md
```

---

## 🧑‍💻 Developer Notes

- Designed for simplicity and educational purposes.  
- Uses CSV files instead of databases for easier setup and portability.  

---

## 💡 Acknowledgments

- Developed using **PyQt5** and **Qt Designer**.
- Developed the UI/UX design with the help of @Shayne-Frances
