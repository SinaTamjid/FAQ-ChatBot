from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QMainWindow, QMessageBox,
    QAction, QHBoxLayout, QVBoxLayout,QWidget,QSizePolicy,
    QSpacerItem,QTextEdit
)
from PyQt5.QtGui import QTextOption,QIcon,QFont
from PyQt5.QtCore import Qt
import sys
import difflib
from Model.main import load_FAQ,normalize

send_icon=r"Icons\send.png"
textpath=r"FAQ.txt"

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.faq_data=load_FAQ(filepath=textpath)
        self.setMinimumSize(800, 500)
        self.setWindowTitle("ChatBot")
        self.UI()

    def UI(self):
        central_wgt=QWidget()
        central_wgt.setStyleSheet("""QWidget {background-color:#c2c2d6}""")
        
        main_layout=QVBoxLayout()
        main_layout.addStretch()
        main_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Expanding, QSizePolicy.Expanding))

        label = QLabel("Hello and Welcome")
        label.setFont(QFont("Kristen ITC", 20, QFont.Bold))
        label.setStyleSheet("""
               QLabel {
               color: #2c3e50;
               border-radius: 10px;
               padding: 10px;
               margin: 10px;
               }
               """)
        main_layout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        main_layout.addStretch()
         
        form_wgt=QWidget()
        form_layout=QHBoxLayout(form_wgt)
        form_layout.setContentsMargins(0,0,0,0)
        form_layout.setSpacing(5)

        self.text_box=QTextEdit()
        self.text_box.setPlaceholderText("Message Me!!")
        self.text_box.setFixedHeight(80)
        self.text_box.setStyleSheet("""
               QTextEdit {
               border: 2px solid #555;
               border-radius: 10px;
               padding: 6px;
               font-size: 16px;
               background-color: #f9f9f9;
               }
               """)
        option = QTextOption()
        option.setWrapMode(QTextOption.WordWrap)
        self.text_box.document().setDefaultTextOption(option)
        self.send=QPushButton()
        self.send.setFixedSize(30,30)
        self.send.setIcon(QIcon(send_icon))
        self.send.setIconSize(self.send.size())
        self.send.setStyleSheet("border: none;") 

        form_layout.addWidget(self.text_box)
        form_layout.addWidget(self.send)
        main_layout.addStretch() 
        main_layout.addWidget(form_wgt)
        
        self.send.clicked.connect(self.SendSection)
        central_wgt.setLayout(main_layout)
        self.setCentralWidget(central_wgt)
    
    def SendSection(self):
        user_msg=self.text_box.toPlainText().strip()
        if not user_msg:
            QMessageBox.warning(self,"Warning","Please Enter a Message.")
            return
        
        response= self.get_bot_response(user_msg)
        if response:
            QMessageBox.information(self,"Bot Answer:\n",response)
        else:
            QMessageBox.warning(self,"Warning","I can't Answer Your Question!")
    
    def get_bot_response(self,msg):
        msg=normalize(msg)
        matches=difflib.get_close_matches(msg,self.faq_data.keys(),n=1,cutoff=0.6)
        if matches:
            return self.faq_data[matches[0]]
        return QMessageBox.warning(self,"Error","I can't Answer Your Question!")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
