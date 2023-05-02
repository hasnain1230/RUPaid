import sys
from datetime import timedelta, datetime

import mariadb
from PyQt5 import QtCore, QtWidgets

from src.RUPaid.DatabaseConnection import DBConnection
from src.RUPaid.Crypt import Hashing
from src.employer.EmployerView import EmployerView
import copy


class EmployerController:
    def __init__(self, employer_data, database_connection: DBConnection):
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
        self.db_connection = database_connection
        self.login_page = None

        self.ui = EmployerView(self)
        self.ui.show()

    def get_all_users(self):
        self.db_connection.commit_transaction()  # Commit any changes to the database and reset the cursor
        query = "SELECT user_id, user_name, first_name, last_name, role, age, occupation, hourly_pay, email, " \
                "bankAccountNumber, bankRoutingNumber FROM users WHERE company_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (self.company_name_id,))

        # Reset the cursor
        self.db_connection.commit_transaction()

        return cursor.fetchall()

    def update_user(self, user_id, column, value):
        query = f"UPDATE users SET {column} = ? WHERE user_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (value, user_id))
        self.db_connection.commit_transaction()

    def pay_user(self, user_id):
        # Get all the time diffs for the users from the clock_in_out table and round them to the nearest 15 minutes
        query = "SELECT id, time_diff FROM clock_in_out WHERE user_id = ? AND paid = 0"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (user_id,))
        time_diffs = cursor.fetchall()

        if len(time_diffs) == 0:
            QtWidgets.QMessageBox.critical(self.ui, "Error", "No time worked to pay the user for.")
            return

        rounded_time_diffs = [self.round_to_nearest_minutes(time_diff[1], 15 * 60) for time_diff in time_diffs]

        start_time = rounded_time_diffs[0]
        total_time_worked = timedelta()

        for time_diff in rounded_time_diffs[1:]:
            total_time_worked += (time_diff - start_time)
            start_time = time_diff

        # For all the IDs in time_diffs, set paid to 1
        query = "UPDATE clock_in_out SET paid = 1 WHERE id = ?"
        cursor = self.db_connection.get_cursor()

        for time_diff in time_diffs:
            cursor.execute(query, (time_diff[0],))

        # Get the hourly pay of the user
        query = "SELECT hourly_pay FROM users WHERE user_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (user_id,))
        hourly_pay = cursor.fetchone()[0]

        # Calculate the total amount to pay the user
        total_amount = total_time_worked.total_seconds() / 3600 * hourly_pay

        # Insert the payment into the pay_user table
        query = "INSERT INTO pay_user (user_id, payment_date, payment_amount, time_pay_period) VALUES (?, NOW(), ?, ?)"
        cursor = self.db_connection.get_cursor()
        # Convert total_time_worked to HH:MM:SS
        total_time_worked = self.timedelta_to_datetime_str(total_time_worked).strftime("%H:%M:%S")

        cursor.execute(query, (user_id, total_amount, total_time_worked))

        self.db_connection.commit_transaction()

        return total_amount

    def timedelta_to_datetime_str(self, td):
        epoch = datetime(1900, 1, 1)
        dt = epoch + td
        return dt

    def get_user_clock_in_history(self, user_id):
        query = "SELECT * FROM clock_in_out WHERE user_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    def get_user_payment_history(self, user_id):
        query = "SELECT * FROM pay_user WHERE user_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    def round_to_nearest_minutes(self, dt, minutes):
        seconds = (dt - dt.min).seconds
        rounding = (seconds + minutes // 2) // minutes * minutes
        return dt + timedelta(0, rounding - seconds, -dt.microsecond)

    def get_next_user_id(self):
        query = "SELECT AUTO_INCREMENT " \
                "FROM information_schema.TABLES " \
                "WHERE TABLE_SCHEMA = 'RUPaid' AND TABLE_NAME = 'users';"

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        user_id = cursor.fetchone()[0]
        return user_id

    def update_password(self, password, user_id):
        query = "UPDATE users SET password = ? WHERE user_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (Hashing.hash_password(password), user_id))
        self.db_connection.commit_transaction()

    def check_for_duplicate_username(self, username):
        query = "SELECT user_name FROM users WHERE user_name = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (username,))
        return cursor.fetchone() is not None

    def edit_employee(self, user_id, username, first_name, last_name, role, age, occupation, hourly_pay, email,
                      bank_account, bank_routing_number):
        self.db_connection.commit_transaction()

        # Check if bank account number has *'s in it
        if "*" in bank_account:
            # Get bank account of user_id
            query = "SELECT bankAccountNumber FROM users WHERE user_id = ?"
            cursor = self.db_connection.get_cursor()
            cursor.execute(query, (user_id,))
            bank_account = cursor.fetchone()[0]

        query = "UPDATE users SET user_name = ?, first_name = ?, last_name = ?, role = ?, age = ?, occupation = ?, hourly_pay = ?, email = ?, bankAccountNumber = ?, bankRoutingNumber = ? WHERE user_id = ?"
        cursor = self.db_connection.get_cursor()
        cursor.execute(query, (
        username, first_name, last_name, role, age, occupation, hourly_pay, email, bank_account, bank_routing_number,
        user_id))
        self.db_connection.commit_transaction()
        self.ui.populate_table()

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
