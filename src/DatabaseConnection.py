import sys

import mariadb
from PyQt5.QtWidgets import QMessageBox, QWidget


class DBConnection(QWidget):
    def __init__(self):
        super().__init__()
        try:
            self.db = mariadb.connect(
                user='RUPaid',
                password='RUPaid',
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

    def commit_transaction(self):
        self.db.commit()
