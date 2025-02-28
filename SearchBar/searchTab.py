from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QFocusEvent


class SearchBar(QLineEdit): 
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setPlaceholderText("Search")
        self.setStyleSheet("color: gray;")

    def focusInEvent(self, event: QFocusEvent):
        if self.text() == self.placeholderText():
            self.clear()
            self.setStyleSheet("""background-color: white; 
                                     border: 1px solid peru; 
                                     border-radius: 9px; 
                                     padding: 2px;
                                     color: black;  
                                     font-family: "Fixedsys";
                                     font-size: 12px;""")
        else:
            self.setStyleSheet("""background-color: white; 
                                     border: 1px solid peru; 
                                     border-radius: 9px; 
                                     padding: 2px;
                                     color: black; 
                                     font-family: "Fixedsys";
                                     font-size: 12px;""")
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        if self.text() == "":
            self.setPlaceholderText("Search")
            self.setStyleSheet("""background-color: white; 
                                   border: 3px solid peru; 
                                   border-radius: 9px; 
                                   padding: 2px;
                                   color: gray;  /* Placeholder text color */
                                   font-family: "Fixedsys";
                                   font-size: 12px;""")
        super().focusOutEvent(event)
