import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from constants import constants
import mariadb
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from ScaledPixmapLabel import ScaledPixmapLabel
from dbConnection import DBConnection
from employeeController import EmployeeMainController
from src.employerController import EmployerMainController


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        database_connection = DBConnection()
        self.cursor = database_connection.get_cursor()
        self.username_input = None
        self.password_input = None
        self.login_button = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(constants.LOGIN_PAGE)

        layout = QGridLayout()

        self.setFixedSize(513, 369)

        RUPAID_logo = ScaledPixmapLabel("../assets/RUPaid.png")
        RUPAID_logo.setMinimumSize(493, 185)
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

    def hash_password(self, password):
        digest = hashes.Hash(hashes.SHA3_512(), backend=default_backend())
        digest.update(password.encode())
        return digest.finalize().hex()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        hashed_password = self.hash_password(password)

        try:
            self.cursor.execute("SELECT * FROM users WHERE user_name = ? AND password = ?", (username, hashed_password))
            results = self.cursor.fetchone()
        except mariadb.Connection.Error as e:
            QMessageBox.warning(self, "Error", f"Error connecting to database: {e}")
            return

        if results is not None:
            print("Login successful")
            QMessageBox.information(self, "Login successful", "Login successful")

            if results[7].lower() == "employee":
                self.employee_controller = EmployeeMainController()
                self.employee_controller.show()
                self.close()
            elif results[7].lower() == "employer":
                self.employer_controller = EmployerMainController()
                self.employer_controller.show()
                self.close()
                
        else:
            print("Login failed")
            QMessageBox.warning(self, "Login failed!", "Login failed! Either your username or password is incorrect.")

    def resizeEvent(self, event):
        # This method is called when the window is resized
        # You can add your resize listener logic here
        print(f"Window resized: {event.size()}")

        # Call the parent class's resizeEvent method
        super().resizeEvent(event)
