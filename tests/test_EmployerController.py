import sys
sys.path.append('src')

from src.employer.EmployerController import *
import pytest
from PyQt5 import QtCore, QtGui, QtTest, QtWidgets
from PyQt5.QtCore import QCoreApplication, QObject, Qt
from PyQt5.QtWidgets import *
from pytestqt.plugin import QtBot
from src.RUPaid.DatabaseConnection import *

test_employer=["test_company",30,60,"test_user","test_pass","test_first",
                        "test_last","employer",30,"test_occupation",
                        "test_email","28641842241","256798359",50]

test_new_employee=['test_new_employee', 'e7f21333547181ac07f4aac7772bac550601e6153fddcd91a0dcf9b4b8c3dab8045dadbf56d88ae3736758b8e718268735ae6d00eb73131e8db42857c24a6d63', 'Test_employee', 'Test_employee', 'employee', 30, 'Software Engineer', 'email@domain.com', '2334745811', '2956235235', 20.0]
test_new_employee_dup=['test_new_employee2', 'e7f21333547105ac07f4aac7772bac550601e6153fddcd91a0dcf9b4b8c3dab8045dadbf56d88ae3736758b8e718268735ae6d00eb73131e8db42857c24a6d63', 'Test_employee2', 'Test_employee2', 'employee', 30, 'Software Engineer', 'email2@domain.com', '2334245811', '2956238235', 25.0]
# Make a QApplication instance
app = QApplication(sys.argv)
connection=DBConnection()

def test_init():
    controller = EmployerController(test_employer, connection, True)
    assert controller!=None and controller.employer_data==test_employer

def test_get_all_users():
    controller = EmployerController(test_employer, connection, True)
    actual=controller.get_all_users()
    cursor = connection.get_cursor()
    cursor.execute(f"SELECT * FROM users where company_id=?",(controller.company_name_id,))
    expected = cursor.fetchall()
    assert len(expected)==len(actual)

def test_add_user_duplicate():
    controller = EmployerController(test_employer, connection, True)
    controller.add_user(test_new_employee[0],test_new_employee[1],test_new_employee[2],test_new_employee[3],test_new_employee[4],test_new_employee[5],test_new_employee[6],test_new_employee[7],test_new_employee[8],test_new_employee[9],test_new_employee[10])
    result=controller.add_user(test_new_employee[0],test_new_employee[1],test_new_employee[2],test_new_employee[3],test_new_employee[4],test_new_employee[5],test_new_employee[6],test_new_employee[7],test_new_employee[8],test_new_employee[9],test_new_employee[10])
    assert result==1

def test_remove_user_valid():
    controller = EmployerController(test_employer, connection, True)
    cursor=connection.get_employee_by_name(first=test_new_employee[2],last=test_new_employee[3])
    id=cursor.fetchone()
    result = controller.remove_user(user_id=id[2])
    assert result==True

def test_add_user_valid():
    controller = EmployerController(test_employer, connection, True)
    result=controller.add_user(test_new_employee[0],test_new_employee[1],test_new_employee[2],test_new_employee[3],test_new_employee[4],test_new_employee[5],test_new_employee[6],test_new_employee[7],test_new_employee[8],test_new_employee[9],test_new_employee[10])
    assert result==0

def test_remove_nonexistent_user():
    controller = EmployerController(test_employer, connection, True)
    assert controller.remove_user(user_id=-9999)

def test_logout():
    controller = EmployerController(test_employer, connection, True)
    assert controller.logout()

