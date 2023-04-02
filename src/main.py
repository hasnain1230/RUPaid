import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from constants import constants


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.username_input = None
        self.password_input = None
        self.login_button = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(constants.LOGIN_PAGE)

        layout = QGridLayout()

        RUPAID_logo = QLabel()
        RUPAID_logo.setPixmap(QPixmap("../assets/test1.png")) # This is just a temporary logo I made with some AI image generator
        RUPAID_logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(RUPAID_logo, 0, 0)

        username_label = QLabel(constants.USERNAME_LABEL)
        username_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(username_label, 1, 0)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(constants.USERNAME_LABEL)
        layout.addWidget(self.username_input, 2, 0)

        password_label = QLabel(constants.PASSWORD_LABEL)
        password_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(password_label, 3, 0)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(constants.PASSWORD_LABEL)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.login)
        layout.addWidget(self.password_input, 4, 0)

        self.login_button = QPushButton(constants.LOGIN_BUTTON)
        self.login_button.clicked.connect(self.login)

        layout.addWidget(self.login_button, 5, 0)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "password":
            QMessageBox.information(self, "Success", "You have successfully logged in!")
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # What arguments can be passed to QApplication?
    # https://doc.qt.io/qt-5/qapplication.html#QApplication
    login_page = LoginPage()
    # Set the size of the window
    login_page.resize(400, 200)
    login_page.show()
    sys.exit(app.exec_())
