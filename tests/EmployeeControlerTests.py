from src.RUPaid.Crypt import Hashing
from src.employee.EmployeeController import EmployeeController
from src.RUPaid.DatabaseConnection import DBConnection
from PyQt5.QtWidgets import QApplication

import sys

class EmployeeControllerTest():
    def __init__(self, connection: DBConnection) -> None:
        self.connection = connection
        self.test_employee = [
            'Testing',
            1,
            42,
            'hasnain1230',
            'lucidity',
            'Hasnain',
            'Ali',
            'employee',
            21,
            'Software Engineer',
            'hasnain1230@gmail.com',
            '******2864',
            '8974658465'
        ]
        self.controller = EmployeeController(self.test_employee, connection, False)
        
    def run_tests(self):
        self.test_clock_in()
        self.test_clock_out()
        self.test_save_information()
        self.test_update_password()
        
    def test_clock_in(self):
        cursor = self.connection.get_cursor()
        cursor.execute(f"SELECT clock_in_time FROM clock_in_out where user_id = {self.test_employee[2]} order by clock_in_time desc")
        before = cursor.fetchone()

        self.controller.clock_in()
        cursor.execute(f"SELECT clock_in_time FROM clock_in_out where user_id = {self.test_employee[2]} order by clock_in_time desc")
        after = cursor.fetchone()
        assert before < after, "Failed at EmployeeController.clock_in()"
        
    def test_clock_out(self):
        cursor = self.connection.get_cursor()
        cursor.execute(f"SELECT clock_out_time FROM clock_in_out where user_id = {self.test_employee[2]} order by clock_out_time desc")
        before = cursor.fetchone()

        self.controller.clock_out()
        cursor.execute(f"SELECT clock_out_time FROM clock_in_out where user_id = {self.test_employee[2]} order by clock_out_time desc")
        after = cursor.fetchone()
        assert before != None
        assert after != None
        assert before < after, "Failed at EmployeeController.clock_out()"
    
    def test_save_information(self):
        new_data = [
            "newemail@domain.com",
            '12345678',
            '12345678'
        ]
        cursor = self.connection.get_cursor()
        cursor.execute(f"UPDATE users SET email = '{new_data[0]}', bankAccountNumber = '{new_data[1]}', bankRoutingNumber = '{new_data[2]}' WHERE user_id = {self.test_employee[2]}")
        self.connection.commit_transaction()
        cursor.execute(f"Select email, bankAccountNumber, bankRoutingNumber from users where user_id= {self.test_employee[2]}")
        res = cursor.fetchone()
        assert res[0] == new_data[0] and res[1] == new_data[1] and res[2] == new_data[2]
        
    def test_update_password(self):
        new_password = 'lucidity'
        
        self.controller.update_password(new_password)
        query = "UPDATE users SET password = ? WHERE user_id = ?"
        cursor = self.connection.get_cursor()
        cursor.execute(query, (Hashing.hash_password(new_password), self.test_employee[2]))
        self.connection.commit_transaction()
        cursor.execute(f"Select password from users where user_id = {self.test_employee[2]}")
        res = cursor.fetchone()[0]
        
        assert(Hashing.hash_password(new_password) == res)

app = QApplication(sys.argv)
testRunner = EmployeeControllerTest(DBConnection())
testRunner.run_tests()

        