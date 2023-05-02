import re

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget, QMessageBox, \
    QApplication, QHBoxLayout, QComboBox


class AddUser(QMainWindow):
    def __init__(self, new_user_id, controller, refresh_function):
        super().__init__()

        self.setFixedSize(900, 790)
        self.controller = controller
        self.new_user_id = new_user_id

        self.setWindowTitle("Add User")
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.returnPressed.connect(lambda: self.add_user())

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(lambda: self.add_user())

        confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.returnPressed.connect(lambda: self.add_user())

        first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit()
        self.first_name_input.returnPressed.connect(lambda: self.add_user())

        last_name_label = QLabel("Last Name:")
        self.last_name_input = QLineEdit()
        self.last_name_input.returnPressed.connect(lambda: self.add_user())

        role = QLabel("Role:")
        self.role_input = QComboBox()
        self.role_input.addItems(["Employee", "Employer"])

        age = QLabel("Age:")
        self.age_input = QLineEdit()
        age_validator = QtGui.QIntValidator()
        self.age_input.setValidator(age_validator)
        self.age_input.returnPressed.connect(lambda: self.add_user())

        occupation = QLabel("Occupation:")
        self.occupation_input = QLineEdit()
        self.occupation_input.returnPressed.connect(lambda: self.add_user())

        email = QLabel("Email:")
        self.email_input = QLineEdit()
        email_validator = QtGui.QRegExpValidator(QRegExp(r"[^@]+@[^@]+\.[^@]+"))
        self.email_input.setValidator(email_validator)
        self.email_input.returnPressed.connect(lambda: self.add_user())

        bank_account = QLabel("Bank Account:")
        self.bank_account_input = QLineEdit()
        bank_account_validator = QtGui.QIntValidator()
        self.bank_account_input.setValidator(bank_account_validator)
        self.bank_account_input.returnPressed.connect(lambda: self.add_user())

        bank_routing_number = QLabel("Bank Routing Number:")
        self.bank_routing_number_input = QLineEdit()
        bank_routing_number_validator = QtGui.QIntValidator()
        self.bank_routing_number_input.setValidator(bank_routing_number_validator)
        self.bank_routing_number_input.returnPressed.connect(lambda: self.add_user())

        hourly_rate = QLabel("Hourly Rate:")
        self.hourly_rate_input = QLineEdit()
        hourly_rate_validator = QtGui.QDoubleValidator()
        hourly_rate_validator.setDecimals(2)
        self.hourly_rate_input.setValidator(hourly_rate_validator)
        self.hourly_rate_input.returnPressed.connect(lambda: self.add_user())

        button_layout = QHBoxLayout()

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(lambda: self.add_user())
        button_layout.addWidget(self.add_user_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(lambda: (refresh_function(), self.close()))
        button_layout.addWidget(self.cancel_button)

        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(first_name_label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(last_name_label)
        layout.addWidget(self.last_name_input)
        layout.addWidget(role)
        layout.addWidget(self.role_input)
        layout.addWidget(age)
        layout.addWidget(self.age_input)
        layout.addWidget(occupation)
        layout.addWidget(self.occupation_input)
        layout.addWidget(email)
        layout.addWidget(self.email_input)
        layout.addWidget(bank_account)
        layout.addWidget(self.bank_account_input)
        layout.addWidget(bank_routing_number)
        layout.addWidget(self.bank_routing_number_input)
        layout.addWidget(hourly_rate)
        layout.addWidget(self.hourly_rate_input)
        layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)

    def add_user(self):
        try:
            username = self.username_input.text()
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()
            first_name = self.first_name_input.text()
            first_name = first_name[0].upper() + first_name[1:].lower()
            last_name = self.last_name_input.text()
            last_name = last_name[0].upper() + last_name[1:].lower()
            role = self.role_input.currentText().lower()
            age = self.age_input.text()
            occupation = self.occupation_input.text()
            email = self.email_input.text()
            bank_account = self.bank_account_input.text()
            bank_routing_number = self.bank_routing_number_input.text()
            hourly_rate = self.hourly_rate_input.text()
        except IndexError:
            QMessageBox.about(self, "Error", "Please fill in all fields : Either first name or last name is empty")
            return

        if not username or not password or not confirm_password or not first_name or not last_name or not role or not age or not occupation or not email or not bank_account or not bank_routing_number or not hourly_rate:
            QMessageBox.about(self, "Error", "Please fill in all fields")
        elif password != confirm_password:
            QMessageBox.about(self, "Error", "Passwords do not match")
        elif int(age) < 18 or int(age) > 100:
            QMessageBox.about(self, "Error", "Invalid age")
        elif float(hourly_rate) < 0.0:
            QMessageBox.about(self, "Error", "Invalid hourly rate")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.about(self, "Error", "Invalid email")
        else:
            success = self.controller.add_user(username, password, first_name, last_name, role, age, occupation, email, bank_account, bank_routing_number, hourly_rate)

            if success == 0:
                self.close()
            elif success == 1:
                QtWidgets.QMessageBox.critical(self, "Error", "Username already exists. Please try again.",
                                               QtWidgets.QMessageBox.Ok)
                return

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        print(self.size())


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    new_user_id = 1  # Replace this with the actual user ID
    controller = None  # Replace this with the actual controller instance

    window = AddUser(new_user_id, controller)
    window.show()

    sys.exit(app.exec_())