import sys

import mariadb
from PyQt5.QtWidgets import QMessageBox, QWidget


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
        
    def commit_transaction(self):
        self.db.commit()
