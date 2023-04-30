import sys

import mariadb
from PyQt5.QtWidgets import QMessageBox, QWidget
from datetime import datetime


class DBConnection(QWidget):
    def __init__(self):
        super().__init__()

        host_names = ['lucidityarch.com', '192.168.1.116']

        self.db = None
        self.cursor = None

        for name in host_names:
            print(name)
            try:
                self.db = mariadb.connect(
                    user='RUPaid',
                    password='RUPaid',
                    host=name,
                    port=3306,
                    database='RUPaid'
                )
                self.cursor = self.db.cursor()
                break
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}. Trying next host...")
                continue

        if self.cursor is None:
            QMessageBox.critical(self, "Connection Error", "Error connecting to database. Please try again later.",
                                 QMessageBox.Ok)
            sys.exit(115)


    def get_cursor(self):
        return self.cursor

    def select_other_users_from_table(self, user_id):
        self.cursor.execute(f'SELECT * FROM users where user_id != {user_id}')
        return self.cursor
    
    def select_names_from_table(self, table='users'):
        self.cursor.execute(f'SELECT firstName, lastName FROM {table}')
        return self.cursor

    def get_employee_by_name(self, first, last, table='users'):
        self.cursor.execute(f"SELECT * from {table} WHERE firstName = '{first}' and lastName = '{last}'")
        return self.cursor

    def update_employee(self, id, first, last, email, urn, account, routing):
        sql = "UPDATE users SET firstName = %s, lastName = %s, email = %s, user_name = %s, bankAccountNumber = %s, bankRoutingNumber = %s WHERE id = %s"
        values = (first, last, email, urn, account, routing, id)
        self.cursor.execute(sql, values)
        self.db.commit()

    def get_employee_conversation(self, sender_id, recipient_id):
        sql = f"SELECT * from messages where (sender_id = {sender_id} and recipient_id = {recipient_id}) or (sender_id = {recipient_id} and recipient_id = {sender_id})"
        self.cursor.execute(sql)
        return self.cursor
    
    def get_user_id_by_name(self, first, last):
        sql = f"SELECT user_id from users where first_name = '{first}' and last_name = '{last}'"
        self.cursor.execute(sql)
        return self.cursor
    
    def insert_message(self, sender_id, recipient_id, message_length, message):
        dateObject= datetime.now()
        time = dateObject.strftime("%Y-%m-%d %H:%M:%S")
        sql = f"INSERT into messages (sender_id, recipient_id, message_length, message, is_checked, date) VALUES ({sender_id}, {recipient_id}, {message_length}, '{message}', 0, '{time}')"

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            # POPUP HERE
            print("Failed to send message")
        return 1
    def commit_transaction(self):
        self.db.commit()
