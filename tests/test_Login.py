from src.RUPaid.Login import *
import sys
from PyQt5.QtWidgets import QApplication, QLineEdit
import src.RUPaid.DatabaseConnection 

app = QApplication(sys.argv)
connection=DBConnection()
cursor = connection.get_cursor()

username_input=QLineEdit()
password_input=QLineEdit()

def test_init():
    login_page = LoginPage(database_connection=connection,test=True)
    assert login_page!=None and login_page.database_connection==connection

def test_login_valid_user_pass_employer():
    login_page = LoginPage(database_connection=connection,test=True)
    username_input.setText('test_user')
    password_input.setText('test_pass')
    login_page.username_input=username_input
    login_page.password_input=password_input
    result=login_page.login()
    assert result==True

def test_login_valid_user_pass_employee():
    login_page = LoginPage(database_connection=connection,test=True)
    username_input.setText('test_employee')
    password_input.setText('test_employee')
    login_page.username_input=username_input
    login_page.password_input=password_input
    result=login_page.login()
    assert result==True

def test_login_valid_employer_invalid_pass():
    login_page = LoginPage(database_connection=connection,test=True)
    username_input.setText('test_user')
    password_input.setText('invalid_pass')
    login_page.username_input=username_input
    login_page.password_input=password_input
    result=login_page.login()
    assert result==False

def test_login_valid_employee_invalid_pass():
    login_page = LoginPage(database_connection=connection,test=True)
    username_input.setText('test_employee')
    password_input.setText('invalid_pass')
    login_page.username_input=username_input
    login_page.password_input=password_input
    result=login_page.login()
    assert result==False

def test_login_invalid_user_invalid_pass():
    login_page = LoginPage(database_connection=connection,test=True)
    username_input.setText('invalid_user')
    password_input.setText('invalid_pass')
    login_page.username_input=username_input
    login_page.password_input=password_input
    result=login_page.login()
    assert result==False