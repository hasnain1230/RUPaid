import sys

import mariadb
from PyQt5.QtWidgets import QMessageBox, QWidget


class DBConnection(QWidget):
    def __init__(self):
        super().__init__()
        try:
            self.db = mariadb.connect(
                user='lucidity',
                password='lucidity',
                host='lucidityarch.com',
                port=3306,
                database='RUPaid'
            )
            self.cursor = self.db.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            QMessageBox.critical(self, "Connection Error", "Error connecting to database. Please try again later.",
                                 QMessageBox.Ok)
            sys.exit(115)

    def get_cursor(self):
        return self.cursor

    def select_names_from_table(self, table='users'):
        self.cursor.execute(f'SELECT first_name, last_name FROM {table}')
        return self.cursor

    def get_employee_by_name(self, first, last, table='users'):
        self.cursor.execute(f"SELECT * from {table} WHERE first_name = '{first}' and last_name = '{last}'")
        return self.cursor

    def update_employee(self, id, first, last, email, urn, account, routing):
        sql = "UPDATE users SET first_name = %s, last_name = %s, email = %s, user_name = %s, bankAccountNumber = %s, bankRoutingNumber = %s WHERE id = %s"
        values = (first, last, email, urn, account, routing, id)
        self.cursor.execute(sql, values)
        self.db.commit()

    def get_messages(self, userid):
        sql = f"SELECT * FROM messages WHERE user_id = '{userid}'"
        self.cursor.execute(sql)
        return self.cursor
    
    def insert_msg(self, userid, msglength, msg):
        sql = f"INSERT INTO messages (user_id, message_length, message, is_checked) VALUES ({userid}, {msglength}, '{msg}', 0)"
        self.cursor.execute(sql)
        self.db.commit()
        return