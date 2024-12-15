from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMessageBox, QLineEdit, QPushButton, QMessageBox, QMainWindow, QStackedWidget, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6 import uic
import sys
import csv
from setup_db import *

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
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")
        
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))
        
    def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))

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

        user = get_user_by_email_and_password(email, password)        
        if user is not None:
            msg.success_box("Đăng nhập thành công")
            self.show_home(user["id"])
            return
        
        msg.error_box("Email hoặc mật khẩu không đúng")
    
    def show_home(self, user_id):
        self.home = Home(user_id)
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
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")
        self.btn_eye_cp = self.findChild(QPushButton, "btn_eye_cp")
        
        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))
        self.btn_eye_cp.clicked.connect(lambda: self.hiddenOrShow(self.confirm_password, self.btn_eye_cp))
        
    def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
        
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

        check_email = get_user_by_email(email)
        if check_email is not None:
            msg.error_box("Email đã tồn tại")
            return

        create_user(name, email, password)
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
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("ui/item.ui", self)
        
        self.user_id = user_id
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
        self.txt_nationality = self.findChild(QLineEdit, "txt_nationality")
        self.txt_age = self.findChild(QLineEdit, "txt_age")
        self.cb_gender = self.findChild(QComboBox, "cb_gender")

        user = get_user_by_id(self.user_id)
        print(user)
        self.txt_name.setText(user["name"])
        self.txt_email.setText(user["email"])
        self.txt_nationality.setText(user["nationality"])
        self.txt_age.setText(user["age"])
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()

