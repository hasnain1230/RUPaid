from src.employee.EmployeeController import *
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import src.RUPaid.Crypt
import src.RUPaid.DatabaseConnection 

password='test_pass2'
password_hash = src.RUPaid.Crypt.Hashing.hash_password(password)

employee_data_test=['test_company', 30, 62, 'test_employee', 'e7f21333547181ac07f4aac7772bac550601e6153fddcd91a0dcf9b4b8c3dab8045dadbf56d88ae3736758b8e718268735ae6d00eb73131e8db42857c24a6d63', 'Test_employee', 'Test_employee', 'employee', 30, 'Software Engineer', 'employee@outlook.com', '2334745811', '2956235235', 20.0]

# Make a QApplication instance
app = QApplication(sys.argv)
connection=DBConnection()

def test_init():
    controller=EmployeeController(employee_data_test, connection, True)
    assert controller!=None and controller.employee_data==employee_data_test and controller.db_connection==connection

def test_connection():
    assert connection!=None

#def test_save_information():
#    controller = EmployeeController(employee_data_test, connection)
#    controller.save_information()
#    assert True

def test_clock_in():
    controller=EmployeeController(employee_data_test, connection, True)
    controller.clock_in()
    query = "SELECT user_id, clock_in_time, clock_out_time FROM clock_in_out WHERE user_id=? AND clock_in_time=NOW();"
    cursor=connection.get_cursor()
    cursor.execute(query, (controller.user_id,))
    result=cursor.fetchall()
    assert len(result)==1

def test_clock_out():
    assert True

def test_get_time_checked_in():
    assert True

def test_check_password():
    assert True

def test_update_password():
    assert True

def test_logout():
    assert True

test_clock_in()

