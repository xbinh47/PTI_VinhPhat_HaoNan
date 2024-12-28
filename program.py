from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from PyQt6.QtCore import *
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

class MovieItemWidget(QWidget):
    signal_detail_movie = QtCore.pyqtSignal(int)
    def __init__(self, id, name, image_path):
        super().__init__()
        uic.loadUi("ui/item.ui", self)
        self.id = id
        self.name = name
        self.image_path = image_path

        self.lbl_name = self.findChild(QLabel, 'lbl_name')
        self.btn_detail = self.findChild(QPushButton, 'btn_detail')
        self.lbl_image = self.findChild(QLabel, 'lbl_image')
        self.lbl_name.setText(name)
        self.lbl_image.setPixmap(QPixmap(image_path))
        self.btn_detail.clicked.connect(self.handle_detail_movie)
        
        self.setMinimumSize(300, 550)

    def handle_detail_movie(self):
        self.signal_detail_movie.emit(self.id)
class Home(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("ui/home.ui", self)
        
        self.user_id = user_id
        self.movie_id = None
        self.stackWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.accountBtn = self.findChild(QPushButton, "btn_account")
        self.watchBtn = self.findChild(QPushButton, "btn_watch")
        self.homeBtn = self.findChild(QPushButton, "btn_home")
        self.savedBtn = self.findChild(QPushButton, "btn_saved")
        self.saveBtn = self.findChild(QPushButton, "btn_save")
        self.avatar_btn = self.findChild(QPushButton, "avatar_btn")
        self.movieList = self.findChild(QScrollArea, 'movieList')
        self.search_bar = self.findChild(QLineEdit, "search_bar")
        self.search_bar.textChanged.connect(self.search_movie)
        
        # ui
        self.movieItem = QWidget()
        self.gridLayout = QGridLayout(self.movieItem)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)

        self.movieItem.setLayout(self.gridLayout)

        self.movieList.setWidget(self.movieItem)
        self.movieList.setWidgetResizable(True)
        
        # media player
        self.lbl_title = self.findChild(QLabel, 'videoName')
        self.volumeBtn = self.findChild(QPushButton, 'volumeBtn')
        self.timeLabel = self.findChild(QLabel, 'timeLabel')
        self.durationBar = self.findChild(QSlider, 'durationBar')
        self.volumeBar = self.findChild(QSlider, 'volumeBar')
        self.videoName = self.findChild(QLabel, 'videoName')
        self.playBtn = self.findChild(QPushButton, 'playBtn')
        self.playIcon = QIcon("img/play-solid.svg")
        self.pauseIcon = QIcon("img/pause-solid.svg")
        self.volumeHighIcon = QIcon("img/volume-high-solid.svg")
        self.volumeLowIcon = QIcon("img/volume-low-solid.svg")
        self.volumeOffIcon = QIcon("img/volume-off-solid.svg")
        self.btn_play_video = self.findChild(QPushButton, 'btn_play_video')
        self.playBtn.setIcon(self.playIcon)
        self.volumeBtn.setIcon(self.volumeHighIcon)
        # Ensure volume bar range is set from 0 to 100
        self.current_volume = 50
        self.volumeBar.setValue(self.current_volume)
        self.volumeBar.setRange(0, 100)
        self.volumeBar.setValue(50)  # Set initial volume to 50%
        # Connect QPushButton and QToolButton clicks to methods
        self.playBtn.clicked.connect(self.play)
        self.volumeBtn.clicked.connect(self.toggleMute)
        
        # Create a QVideoWidget object
        placeholder = self.findChild(QWidget, 'videoWidget')
        self.videoWidget = QVideoWidget()
        self.videoWidget.setGeometry(placeholder.geometry())
        self.videoWidget.setParent(placeholder.parentWidget())
        placeholder.hide()
        self.mediaPlayer = QMediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.audioOutput = QAudioOutput(self)
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        
        self.accountBtn.clicked.connect(self.navigateAccountScreen)
        self.homeBtn.clicked.connect(self.navigateHomeScreen)
        self.savedBtn.clicked.connect(self.navigateSavedScreen)
        self.watchBtn.clicked.connect(self.navigateWatchScreen)
        self.btn_play_video.clicked.connect(self.loadVideo)
        self.stackWidget.setCurrentIndex(2)
        self.renderAccountScreen()
        self.renderMovieList(get_all_movies())
        self.saveBtn.clicked.connect(self.changeAccountInfo)
        self.avatar_btn.clicked.connect(self.loadAvatarFromFile)

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
        self.avatar_btn = self.findChild(QPushButton, "avatar_btn")

        self.user = get_user_by_id(self.user_id)
        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.txt_nationality.setText(self.user["nationality"])
        self.txt_age.setText(str(self.user["age"]))
        if self.user["gender"] == "Male":
            self.cb_gender.setCurrentIndex(0)
        elif self.user["gender"] == "Female":
            self.cb_gender.setCurrentIndex(1) 
        else:
            self.cb_gender.setCurrentIndex(2)
        if self.user["avatar"] != "":
            self.avatar_btn.setIcon(QIcon(self.user["avatar"]))
    
    def changeAccountInfo(self):
        name = self.txt_name.text()
        email = self.txt_email.text()
        nationality = self.txt_nationality.text()
        age = self.txt_age.text()
        if self.cb_gender.currentIndex() == 0:
            gender = "Male"
        elif self.cb_gender.currentIndex() == 1:
            gender = "Female"
        else:
            gender = "Other"
        avatar = self.user["avatar"]
        u = User(name, email, "", nationality, age, gender, avatar)
        
        update_user(self.user_id, u)
        self.renderAccountScreen()

    def loadAvatarFromFile(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *jpeg *.bmp)")
        if file:
            self.user["avatar"] = file
            self.avatar_btn.setIcon(QIcon(file))
            
    def renderMovieList(self, movie_list:list):
        # Clear previous search results
        for i in reversed(range(self.gridLayout.count())):
            widgetToRemove = self.gridLayout.itemAt(i).widget()
            self.gridLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
            
        row = 0
        column = 0
        for movie in movie_list:
            itemWidget = MovieItemWidget(movie["id"], movie["name"], movie["image_path"])
            itemWidget.signal_detail_movie.connect(self.catch_detail_movie)
            self.gridLayout.addWidget(itemWidget, row, column)
            column += 1
            if column == 3:
                row += 1
                column = 0
    
    def search_movie(self):
        name = self.search_bar.text()
        movie_list = get_movie_by_name(name)
        self.renderMovieList(movie_list)

    def detail_movie(self, movie_id):
        movie = get_movie_by_id(movie_id)
        self.lbl_name = self.findChild(QLabel, "lbl_detail_name")
        self.lbl_duration = self.findChild(QLabel, "lbl_detail_duration")
        self.lbl_type = self.findChild(QLabel, "lbl_detail_type")
        self.lbl_country = self.findChild(QLabel, "lbl_detail_country")
        self.lbl_description = self.findChild(QLabel, "lbl_detail_description")
        self.lbl_release_date = self.findChild(QLabel, "lbl_detail_release_date")
        self.lbl_image = self.findChild(QLabel, "lbl_detail_image")
        
        self.lbl_name.setText(movie["name"])
        self.lbl_duration.setText(f"Duration: {movie['duration']}")
        self.lbl_type.setText(f"Type: {movie['type']}")
        self.lbl_country.setText(f"Country: {movie['country']}")
        self.lbl_release_date.setText(f"Release Date: {movie['release_date']}")
        self.lbl_image.setPixmap(QPixmap(movie["image_path"]))
        
        # Fix the description formatting
        description = movie["description"]
        split_description = description.split(" ")
        # First join words in each chunk with spaces, then join chunks with newlines
        description = "\n".join([" ".join(split_description[i:i+10]) for i in range(0, len(split_description), 10)])
        self.lbl_description.setText(f"Description: {description}")
        
    def loadVideo(self):
        if self.movie_id is None:
            return
        try:
            movie = get_movie_by_id(self.movie_id)
            self.mediaPlayer.setSource(QUrl.fromLocalFile(movie["file_path"]))
            self.mediaPlayer.play()
            self.lbl_title.setText(movie["name"])
            self.durationBar.sliderMoved.connect(self.setPosition)
            self.volumeBar.sliderMoved.connect(self.setVolume)
            self.mediaPlayer.playbackStateChanged.connect(self.mediaStateChanged)
            self.mediaPlayer.positionChanged.connect(self.positionChanged)
            self.mediaPlayer.durationChanged.connect(self.durationChanged)
            self.mediaPlayer.errorOccurred.connect(self.handleError)
            self.stackWidget.setCurrentIndex(3)
        except Exception as e:
            print(f"Error loading video: {e}")
        
    def mediaStateChanged(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playBtn.setIcon(self.pauseIcon)
        else:
            self.playBtn.setIcon(self.playIcon)

    def positionChanged(self, position):
        self.durationBar.setValue(position)
        # Convert position and duration from milliseconds to hh:mm:ss format
        current_time = self.formatTime(position)
        total_time = self.formatTime(self.mediaPlayer.duration())
        self.timeLabel.setText(f"{current_time}/{total_time}")
        
    def durationChanged(self, duration):
        self.durationBar.setRange(0, duration)
    
    def handleError(self):
        self.playBtn.setEnabled(False)
        error_message = self.mediaPlayer.errorString()
        self.playBtn.setText(f"Error: {error_message}")
        print(f"Media Player Error: {error_message}")
        
    def play(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    def setVolume(self, volume):
        # Convert the slider value to a float between 0.0 and 1.0
        volume = volume / 100.0
        self.audioOutput.setVolume(volume)
        if volume == 0.0:
            self.volumeBtn.setIcon(self.volumeOffIcon)
        elif volume < 0.5:
            self.audioOutput.setMuted(False)
            self.volumeBtn.setIcon(self.volumeLowIcon)
        else:
            self.volumeBtn.setIcon(self.volumeHighIcon)
            self.audioOutput.setMuted(False)
    
    def toggleMute(self):
        if self.audioOutput.isMuted():
            self.audioOutput.setMuted(False)
            if self.current_volume >= 50:
                self.volumeBtn.setIcon(self.volumeHighIcon)
            elif self.current_volume < 50:
                self.volumeBtn.setIcon(self.volumeLowIcon)
            else:
                self.volumeBtn.setIcon(self.volumeOffIcon)
            self.volumeBar.setValue(self.current_volume)
        else:
            self.audioOutput.setMuted(True)
            self.volumeBtn.setIcon(self.volumeOffIcon)
            self.current_volume = self.volumeBar.value()
            self.volumeBar.setValue(0)
    
    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def formatTime(self, milliseconds):
        total_seconds = milliseconds // 1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    @QtCore.pyqtSlot(int)
    def catch_detail_movie(self, movie_id):
        self.movie_id = movie_id
        self.detail_movie(self.movie_id)
        self.stackWidget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window = Home(1)
    window.show()
    app.exec()

