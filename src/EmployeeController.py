from PyQt5 import QtWidgets
from EmployeeView import EmployeeView
from DatabaseConnection import DBConnection


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
        self.account_number = employee_data[11]
        self.routing_number = employee_data[12]
        self.db_connection = DBConnection()

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

    def get_time_checked_in(self, user_id):
        query = "SELECT clock_in_time FROM clock_in_out WHERE user_id = ? ORDER BY clock_in_time DESC LIMIT 1"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchone()[0]

    def logout(self):
        self.ui.close()
        from Login import LoginPage
        # Load the login page
        self.login_page = LoginPage()
        self.login_page.show()
