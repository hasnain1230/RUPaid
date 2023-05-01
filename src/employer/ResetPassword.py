from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget, QMessageBox


class ResetPassword(QMainWindow):
    def __init__(self, user_id_to_reset, employer_controller):
        super().__init__()

        self.user_id_to_reset = user_id_to_reset
        self.employer_controller = employer_controller

        self.setWindowTitle("Password Change")
        self.setFixedSize(580, 170)
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        new_password_label = QLabel("New Password:")
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.returnPressed.connect(self.update_password)

        confirm_password_label = QLabel("Confirm New Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.returnPressed.connect(self.update_password)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.update_password)

        layout.addWidget(new_password_label)
        layout.addWidget(self.new_password_input)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(submit_button)

        self.setCentralWidget(central_widget)
        self.show()


    def update_password(self):
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Check if any of the fields are empty
        if not new_password or not confirm_password:
            QMessageBox.about(self, "Error", "Please fill out all fields.")
            return
        elif new_password != confirm_password:
            QMessageBox.about(self, "Error", "New passwords do not match")
            self.new_password_input.clear()
            self.confirm_password_input.clear()

            # Set focus to new password input
            self.new_password_input.setFocus()
            return
        else:
            self.employer_controller.update_password(new_password, self.user_id_to_reset)
            QMessageBox.about(self, "Success", "Password successfully updated.")
            self.close()