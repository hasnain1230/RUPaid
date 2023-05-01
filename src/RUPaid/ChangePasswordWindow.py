from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget, QMessageBox


class ChangePasswordWindow(QMainWindow):
    def __init__(self, employee_controller):
        super().__init__()

        self.employee_controller = employee_controller

        self.setWindowTitle("Password Change")
        self.setFixedSize(390, 232)
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        current_password_label = QLabel("Current Password:")
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.returnPressed.connect(self.update_password)

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

        layout.addWidget(current_password_label)
        layout.addWidget(self.current_password_input)
        layout.addWidget(new_password_label)
        layout.addWidget(self.new_password_input)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(submit_button)

        self.setCentralWidget(central_widget)

    def update_password(self):
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Check if any of the fields are empty
        if not current_password or not new_password or not confirm_password:
            QMessageBox.about(self, "Error", "Please fill out all fields.")
            return
        elif not self.employee_controller.check_password(current_password):
            QMessageBox.about(self, "Error",
                              "Current password does not match your previous password. Please speak to your manager to reset your password.")
            QMessageBox.about(self, "Error",
                              "Current password does not match your previous password. Please speak to your manager to reset your password.")

            self.current_password_input.clear()
            self.current_password_input.setFocus()
            return
        elif new_password != confirm_password:
            QMessageBox.about(self, "Error", "New passwords do not match")
            self.new_password_input.clear()
            self.confirm_password_input.clear()

            # Set focus to new password input
            self.new_password_input.setFocus()
            return
        else:
            self.employee_controller.update_password(new_password)
            QMessageBox.about(self, "Success", "Password successfully updated.")
            self.close()
