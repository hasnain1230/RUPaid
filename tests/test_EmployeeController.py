from src.employee.EmployeeController import *
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import src.RUPaid.Crypt
import src.RUPaid.DatabaseConnection 
import pytest

password='test_pass2'
password_hash = src.RUPaid.Crypt.Hashing.hash_password(password)

test_employee=['test_company', 30, 124, 'test_employee', 'e7f21333547181ac07f4aac7772bac550601e6153fddcd91a0dcf9b4b8c3dab8045dadbf56d88ae3736758b8e718268735ae6d00eb73131e8db42857c24a6d63', 'test_first', 'test_last', 'employee', 30, 'Software Engineer', 'email@domain.com', '2334745811', '2956235235', 20.0]

# Make a QApplication instance
app = QApplication(sys.argv)
connection=DBConnection()

def test_init():
    controller=EmployeeController(test_employee, connection, True)
    assert controller!=None and controller.employee_data==test_employee and controller.db_connection==connection

def test_clock_in():
    controller=EmployeeController(test_employee, connection, True)
    cursor = connection.get_cursor()
    cursor.execute(f"SELECT clock_in_time FROM clock_in_out where user_id = {test_employee[2]} order by clock_in_time desc")
    before = cursor.fetchone()

    controller.clock_in()
    cursor.execute(f"SELECT clock_in_time FROM clock_in_out where user_id = {test_employee[2]} order by clock_in_time desc")
    after = cursor.fetchone()
    assert before < after, "Failed at EmployeeController.clock_in()"

def test_clock_out():
    controller=EmployeeController(test_employee, connection, True)
    cursor = connection.get_cursor()
    cursor.execute(f"SELECT clock_out_time FROM clock_in_out where user_id = {test_employee[2]} order by clock_out_time desc")
    before = cursor.fetchone()

    controller.clock_out()
    cursor.execute(f"SELECT clock_out_time FROM clock_in_out where user_id = {test_employee[2]} order by clock_out_time desc")
    after = cursor.fetchone()
    assert before != None
    assert after != None
    assert before < after, "Failed at EmployeeController.clock_out()"

def test_save_information():
    controller=EmployeeController(test_employee, connection, True)
    new_data = [
        "newemail@domain.com",
        '12345678',
        '12345678'
    ]
    cursor = connection.get_cursor()
    cursor.execute(f"UPDATE users SET email = '{new_data[0]}', bankAccountNumber = '{new_data[1]}', bankRoutingNumber = '{new_data[2]}' WHERE user_id = {test_employee[2]}")
    connection.commit_transaction()
    cursor.execute(f"Select email, bankAccountNumber, bankRoutingNumber from users where user_id= {test_employee[2]}")
    res = cursor.fetchone()
    assert res[0] == new_data[0] and res[1] == new_data[1] and res[2] == new_data[2]
    
def test_update_password():
    controller=EmployeeController(test_employee, connection, True)
    new_password = 'test_employee'
    
    controller.update_password(new_password)
    query = "UPDATE users SET password = ? WHERE user_id = ?"
    cursor = connection.get_cursor()
    cursor.execute(query, (Hashing.hash_password(new_password), test_employee[2]))
    connection.commit_transaction()
    cursor.execute(f"Select password from users where user_id = {test_employee[2]}")
    res = cursor.fetchone()[0]
    assert(Hashing.hash_password(new_password) == res)

def test_logout():
    controller = EmployeeController(test_employee, connection, True)
    assert controller.logout()