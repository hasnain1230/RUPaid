from PyQt5 import Qt, QtGui
from PyQt5.QtWidgets import *


class EditDialog(QDialog):
    def __init__(self, table, controller, parent=None):
        super(EditDialog, self).__init__(parent)
        self.table = table
        self.controller = controller
        self.parent = parent
        self.setFixedSize(670, 736)

        # Get selected row
        selected_row = self.table.selectedIndexes()
        # Get user id of selected row

        self.setWindowTitle("Edit Employee")

        self.layout = QVBoxLayout()

        self.user_id = QLabel("User ID")
        self.user_id_input = QLineEdit()
        self.user_id_input.setText(self.table.item(selected_row[0].row(), 0).text())
        self.user_id_input.setReadOnly(True)

        self.username = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setText(self.table.item(selected_row[0].row(), 1).text())

        self.first_name = QLabel("First Name")
        self.first_name_input = QLineEdit()
        self.first_name_input.setText(self.table.item(selected_row[0].row(), 2).text())

        self.last_name = QLabel("Last Name")
        self.last_name_input = QLineEdit()
        self.last_name_input.setText(self.table.item(selected_row[0].row(), 3).text())

        self.role = QLabel("Role")
        self.role_input = QComboBox()
        self.role_input.addItems(["Employee", "Employer"])
        # Set the text such that the first letter is capitalized and the rest are lowercase
        self.role_input.setCurrentText(self.table.item(selected_row[0].row(), 4).text().capitalize())

        self.age = QLabel("Age")
        self.age_input = QLineEdit()
        age_validator = Qt.QIntValidator()
        self.age_input.setValidator(age_validator)
        self.age_input.setText(self.table.item(selected_row[0].row(), 5).text())

        self.occupation = QLabel("Occupation")
        self.occupation_input = QLineEdit()
        self.occupation_input.setText(self.table.item(selected_row[0].row(), 6).text())

        self.hourly_pay = QLabel("Hourly Pay")
        self.hourly_pay_input = QLineEdit()
        self.hourly_pay_input.setValidator(Qt.QDoubleValidator())
        self.hourly_pay_input.setText(self.table.item(selected_row[0].row(), 7).text())

        self.email = QLabel("Email Address")
        self.email_input = QLineEdit()
        email_validator = Qt.QRegExpValidator(Qt.QRegExp(r"[^@]+@[^@]+\.[^@]+"))
        self.email_input.setValidator(email_validator)
        self.email_input.setText(self.table.item(selected_row[0].row(), 8).text())

        self.account_number = QLabel("Account Number")
        self.account_number_input = QLineEdit()
        self.account_number_input.setValidator(Qt.QIntValidator())
        self.account_number_input.setText(self.table.item(selected_row[0].row(), 9).text())

        self.routing_number = QLabel("Routing Number")
        self.routing_number_input = QLineEdit()
        self.routing_number_input.setValidator(Qt.QIntValidator())
        self.routing_number_input.setText(self.table.item(selected_row[0].row(), 10).text())

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)


        self.layout.addWidget(self.user_id)
        self.layout.addWidget(self.user_id_input)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.first_name)
        self.layout.addWidget(self.first_name_input)
        self.layout.addWidget(self.last_name)
        self.layout.addWidget(self.last_name_input)
        self.layout.addWidget(self.role)
        self.layout.addWidget(self.role_input)
        self.layout.addWidget(self.age)
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.occupation)
        self.layout.addWidget(self.occupation_input)
        self.layout.addWidget(self.hourly_pay)
        self.layout.addWidget(self.hourly_pay_input)
        self.layout.addWidget(self.email)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.account_number)
        self.layout.addWidget(self.account_number_input)
        self.layout.addWidget(self.routing_number)
        self.layout.addWidget(self.routing_number_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def submit(self):
        user_id = self.user_id_input.text()
        username = self.username_input.text()
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        role = self.role_input.currentText().lower()
        age = self.age_input.text()
        occupation = self.occupation_input.text()
        hourly_pay = self.hourly_pay_input.text()
        email = self.email_input.text()
        account_number = self.account_number_input.text()
        routing_number = self.routing_number_input.text()

        selected_row = self.table.selectedIndexes()

        if not user_id or not username or not first_name or not last_name or not role or not age or not occupation or not hourly_pay or not email or not account_number or not routing_number:
            QMessageBox.warning(self, "Warning", "Please fill out all fields.")
            return
        elif username != self.table.item(selected_row[0].row(), 1).text() and self.controller.check_for_duplicate_username(username):
            QMessageBox.warning(self, "Warning", "Username already exists.")
            return
        elif int(age) < 18 or int(age) > 100:
            QMessageBox.warning(self, "Warning", "Age must be between 18 and 100.")
            return
        elif float(hourly_pay) < 0:
            QMessageBox.warning(self, "Warning", "Hourly pay must be greater than 0.")
            return
        else:
            self.controller.edit_employee(user_id, username, first_name, last_name, role, age, occupation, hourly_pay, email, account_number, routing_number)
            self.close()
            QMessageBox.information(self, "Success", "Employee edited successfully.")