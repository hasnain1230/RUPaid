import sys
sys.path.append('src')

from src.employer.EmployerController import *
import pytest
from PyQt5 import QtCore, QtGui, QtTest, QtWidgets
from PyQt5.QtCore import QCoreApplication, QObject, Qt
from PyQt5.QtWidgets import *
from pytestqt.plugin import QtBot

employee_data_test=["test_company","test_company_id",30,"test_username","test_password","test_first_name",
                        "test_last_name","employer",30,"test_occupation",
                        "test_email","test_account_number","test_routing_number",]

def test_create(employee_data_test, ):
    controller = EmployerController(employee_data_test)
    assert controller!=None and controller.user_name=="test_username"

#  def test_get_all_users(self):
#      result=EmployerController.get_all_users(self.controller)
#      print(result)
#      self.assertTrue(True)

def test_add_user_valid():
    controller=EmployerController(employee_data_test)
    print(controller)
    assert True

def test_add_user_duplicate():
    assert True

def test_remove_user_valid(controller):
    assert True

def test_remove_nonexistent_user(controller):
    assert True

def test_logout(controller):
    assert True
