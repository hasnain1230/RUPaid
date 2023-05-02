from src.RUPaid.Crypt import Hashing
from src.messaging.MessagingController import MessagingController
from src.RUPaid.DatabaseConnection import DBConnection
from PyQt5.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)
connection=DBConnection()
test_employee = ['Testing',1,42,'hasnain1230','lucidity','Hasnain','Ali','employee',21,'Software Engineer','hasnain1230@gmail.com','**2864','8974658465']

controller = MessagingController(test_employee[2], test_employee[1], False)

def test_wrap_message():
    text_to_be_wrapped = "Wrap this text Wrap this text Wrap this text Wrap this text Wrap this text"
    function_wrapped = controller.wrap_message(text_to_be_wrapped)
    manually_wrapped = ""
    for i, char in enumerate(text_to_be_wrapped):
        if(i %40 == 0):
            manually_wrapped += '\n'
        manually_wrapped += char
    assert function_wrapped==manually_wrapped
