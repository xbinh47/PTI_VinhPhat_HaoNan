from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMessageBox, QLineEdit, QPushButton, QMessageBox, QMainWindow, QStackedWidget, QComboBox
from PyQt6 import uic
import sys
import csv

class MessageBox():
    def success_box(self, message):
        box = QMessageBox()
        box.setWindowTitle("Success")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()
        
    def error_box(self, message):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.exec()

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
        
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)
        
    def login(self):
        msg = MessageBox()
        email = self.email.text()
        password = self.password.text()
        
        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return

        if password == "":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return

        data = []
        with open("data/users.csv", "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        for row in data:
            if row["Email"] == email and row["Password"] == password:
                msg.success_box("Đăng nhập thành công")
                self.show_home(email)
                return
        
        msg.error_box("Email hoặc mật khẩu không đúng")
    
    def show_home(self, email):
        self.home = Home(email)
        self.home.show()
        self.close()   
         
    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()

class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)
        
        self.name = self.findChild(QLineEdit, "txt_name")
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.confirm_password = self.findChild(QLineEdit, "txt_conf_pwd")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        
        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)
        
    def register(self):
        msg = MessageBox()
        name = self.name.text()
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()
        
        if name == "":
            msg.error_box("Họ tên không được để trống")
            self.name.setFocus()
            return
        
        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return

        if password == "":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        
        if confirm_password == "":
            msg.error_box("Xác nhận mật khẩu không được để trống")
            self.confirm_password.setFocus()
            return
        
        if password != confirm_password:
            msg.error_box("Mật khẩu không trùng khớp")
            self.confirm_password.setText("")
            self.password.setFocus()
            return
        
        if not self.validate_email(email):
            msg.error_box("Email không hợp lệ")
            self.email.setFocus()
            return  

        data = []
        with open("data/users.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        for row in data:
            if row["Email"] == email:
                msg.error_box("Email đã tồn tại")
                return

        with open("data/users.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, password, "", "", ""])
        
        msg.success_box("Đăng ký thành công")
        self.show_login()

    def validate_email(self,s):
        idx_at = s.find('@')
        if idx_at == -1:
            return False
        return '.' in s[idx_at+1:]
    
    def show_login(self):   
        self.login = Login()
        self.login.show()
        self.close()
        
class Home(QMainWindow):
    def __init__(self, email):
        super().__init__()
        uic.loadUi("ui/item.ui", self)
        
        self.email = email
        self.stackWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.accountBtn = self.findChild(QPushButton, "btn_account")
        self.watchBtn = self.findChild(QPushButton, "btn_watch")
        self.homeBtn = self.findChild(QPushButton, "btn_home")
        self.savedBtn = self.findChild(QPushButton, "btn_saved")
        self.accountBtn.clicked.connect(self.navigateAccountScreen)
        self.homeBtn.clicked.connect(self.navigateHomeScreen)
        self.savedBtn.clicked.connect(self.navigateSavedScreen)
        self.watchBtn.clicked.connect(self.navigateWatchScreen)
        self.stackWidget.setCurrentIndex(2)
        self.renderAccountScreen()
        
    def navigateAccountScreen(self):
        self.stackWidget.setCurrentIndex(0)

    def navigateSavedScreen(self):
        self.stackWidget.setCurrentIndex(1)
    
    def navigateWatchScreen(self):
        self.stackWidget.setCurrentIndex(3)

    def navigateHomeScreen(self):
        self.stackWidget.setCurrentIndex(2)

    def renderAccountScreen(self):
        self.txt_name = self.findChild(QLineEdit, "txt_name")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_password = self.findChild(QLineEdit, "txt_password")
        self.txt_nationality = self.findChild(QLineEdit, "txt_nationality")
        self.txt_age = self.findChild(QLineEdit, "txt_age")
        self.cb_gender = self.findChild(QComboBox, "cb_gender")

        data = []
        with open("data/users.csv", "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        for row in data:
            if row["Email"] == self.email:
                self.txt_name.setText(row["Name"])
                self.txt_email.setText(row["Email"])
                self.txt_password.setText(row["Password"])
                self.txt_nationality.setText(row["Nationality"])
                self.txt_age.setText(row["Age"])
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()

