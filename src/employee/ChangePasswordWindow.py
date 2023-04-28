import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget


class ChangePasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Change")
        self.setMinimumSize(300, 200)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        self.current_password_label = QLabel("Current Password:")
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.Password)

        self.new_password_label = QLabel("New Password:")
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_label = QLabel("Confirm New Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.submit_button = QPushButton("Submit")

        layout.addWidget(self.current_password_label)
        layout.addWidget(self.current_password_input)
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.submit_button)

        self.setCentralWidget(central_widget)