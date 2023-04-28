from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from src.constants import constants
from ScaledPixmapLabel import ScaledPixmapLabel
from DatabaseConnection import DBConnection
from src.employee.EmployeeController import EmployeeController
from src.RUPaid.Crypt import Hashing
import mariadb


class LoginPage(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.employee_controller = None
        self.employer_controller = None
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

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        hashed_password = Hashing.hash_password(password)

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
                self.close()
                self.employee_controller = EmployeeController(results)
            elif results[7].lower() == "employer":
                pass
                # self.employer_controller = EmployerMainController()

        else:
            print("Login failed")
            QMessageBox.warning(self, "Login failed!", "Login failed! Either your username or password is incorrect.")

    def resizeEvent(self, event):
        # This method is called when the window is resized
        # You can add your resize listener logic here
        print(f"Window resized: {event.size()}")

        # Call the parent class's resizeEvent method
        super().resizeEvent(event)
