from PyQt5 import QtWidgets

from src.RUPaid.Crypt import Hashing
from src.employee.EmployeeView import EmployeeView
from src.RUPaid.DatabaseConnection import DBConnection


class EmployeeController:
    def __init__(self, employee_data):
        self.employee_data = employee_data
        self.company_name = employee_data[0]
        self.company_name_id = employee_data[1]
        self.user_id = employee_data[2]
        self.username = employee_data[3]
        self.password_hash = employee_data[4]
        self.first_name = employee_data[5]
        self.last_name = employee_data[6]
        self.role = employee_data[7]
        self.age = employee_data[8]
        self.occupation = employee_data[9]
        self.email = employee_data[10]
        self.account_number = "*" * (len(employee_data[11]) - 4) + employee_data[11][-4:]
        self.routing_number = employee_data[12]
        self.db_connection = DBConnection()
        self.login_page = None

        self.ui = EmployeeView(self)
        self.ui.show()

    def save_information(self, grid_layout: QtWidgets.QGridLayout):
        # Get the new information from the grid layout
        new_information = {}
        for row in range(5, grid_layout.rowCount()):
            label = grid_layout.itemAtPosition(row, 0).widget()
            value_edit = grid_layout.itemAtPosition(row, 1).widget()

            if isinstance(label, QtWidgets.QLabel) and isinstance(value_edit, QtWidgets.QLineEdit):
                new_information[label.text()] = value_edit.text()

        self.email = new_information["Email:"]
        self.account_number = new_information["Bank Account Number:"]
        self.routing_number = new_information["Bank Routing Number:"]

        # Update the database
        query = "UPDATE users SET email = ?, bankAccountNumber = ?, bankRoutingNumber = ? WHERE user_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (self.email, self.account_number, self.routing_number, self.user_id))
        self.db_connection.commit_transaction()

    def clock_in(self):
        query = "INSERT INTO clock_in_out (user_id, clock_in_time, clock_out_time) VALUES (?, NOW(), NULL)"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (self.user_id,))
        self.db_connection.commit_transaction()

    def clock_out(self):
        query = "UPDATE clock_in_out SET clock_out_time = NOW(), time_diff = TIMEDIFF(clock_out_time, clock_in_time) WHERE user_id = ? AND clock_out_time IS NULL"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (self.user_id,))
        self.db_connection.commit_transaction()

    def get_time_checked_in(self, user_id):
        query = "SELECT clock_in_time FROM clock_in_out WHERE user_id = ? ORDER BY clock_in_time DESC LIMIT 1"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchone()[0]

    def get_time_checked_out(self, user_id):
        query = "SELECT clock_out_time FROM clock_in_out WHERE user_id = ? ORDER BY clock_out_time DESC LIMIT 1"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchone()[0]

    def check_password(self, password):
        query = "SELECT password FROM users WHERE user_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (self.user_id,))
        return cursor.fetchone()[0] == Hashing.hash_password(password)

    def update_password(self, password):
        query = "UPDATE users SET password = ? WHERE user_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (Hashing.hash_password(password), self.user_id))
        self.db_connection.commit_transaction()

    def logout(self, timer=None):
        if timer is not None:
            timer.stop()

        for window in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(window, QtWidgets.QWidget):
                window.close()
        from src.RUPaid.Login import LoginPage
        self.login_page = LoginPage()
        self.login_page.show()

