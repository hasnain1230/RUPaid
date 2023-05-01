import sys

import mariadb
from PyQt5 import QtCore, QtWidgets

from src.RUPaid.DatabaseConnection import DBConnection
from src.RUPaid.Crypt import Hashing
from src.employer.EmployerView import EmployerView


class EmployerController:
    def __init__(self, employer_data):
        self.employee_data = employer_data
        self.company_name = employer_data[0]
        self.company_name_id = employer_data[1]
        self.user_id = employer_data[2]
        self.username = employer_data[3]
        self.password_hash = employer_data[4]
        self.first_name = employer_data[5]
        self.last_name = employer_data[6]
        self.role = employer_data[7]
        self.age = employer_data[8]
        self.occupation = employer_data[9]
        self.email = employer_data[10]
        self.account_number = "*" * (len(employer_data[11]) - 4) + employer_data[11][-4:]
        self.routing_number = employer_data[12]
        self.db_connection = DBConnection()
        self.login_page = None

        self.ui = EmployerView(self)
        self.ui.show()

    def get_all_users(self):
        query = "SELECT user_id, user_name, first_name, last_name, role, age, occupation, hourly_pay, email, " \
                "bankAccountNumber, bankRoutingNumber FROM users WHERE company_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (self.company_name_id,))
        # Bank account number should be *'d out

        return cursor.fetchall()

    def get_next_user_id(self):
        query = "SELECT AUTO_INCREMENT " \
                "FROM information_schema.TABLES " \
                "WHERE TABLE_SCHEMA = 'RUPaid' AND TABLE_NAME = 'users';"

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        return cursor.fetchone()[0]

    def add_user(self, username, password, first_name, last_name, role, age, occupation, email, bank_account,
                 bank_routing_number, hourly_rate):
        query = "INSERT INTO users " \
                "(company_name, company_id, user_name, password, first_name, last_name, role, age, occupation, email, bankAccountNumber, bankRoutingNumber, hourly_pay) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

        cursor = self.db_connection.get_cursor()
        password_hash = Hashing.hash_password(password)
        try:
            cursor.execute(query, (
            self.company_name, self.company_name_id, username, password_hash, first_name, last_name, role, age,
            occupation, email, bank_account, bank_routing_number, hourly_rate))
            self.db_connection.commit_transaction()
            self.ui.populate_table()
            return 0
        except mariadb.IntegrityError:
            return 1
        except mariadb.Error as e:
            QtWidgets.QMessageBox.critical(self.ui, "Error",
                                           f"Error connecting to database. Please try again later. {e}",
                                           QtWidgets.QMessageBox.Ok)
            sys.exit(115)

    def remove_user(self, user_id):
        # Delete user from all tables
        query_list = [
            "DELETE FROM clock_in_out WHERE user_id = ?",
            "DELETE FROM users WHERE user_id = ?",
        ]

        for query in query_list:
            cursor = self.db_connection.get_cursor()
            cursor.execute(query, (user_id,))
            self.db_connection.commit_transaction()
            self.ui.populate_table()

    def logout(self, timer: QtCore.QTimer = None):
        if timer is not None:
            timer.stop()
            print("Timer stopped")

        for window in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(window, QtWidgets.QWidget):
                window.close()

        from src.RUPaid.Login import LoginPage
        self.login_page = LoginPage(self.db_connection)
        self.login_page.show()
