from src.RUPaid.Login import *
import unittest

class LoginTest(unittest.TestCase):

    def test_create(self):
        #login_page = LoginPage()
        self.assertTrue(True)

    def test_login_valid_user_pass_employee(self):

        self.assertTrue(True)
    
    def test_login_valid_user_pass_employer(self):
       self.assertTrue(True)
    

    def test_login_valid_user_invalid_pass(self):
        self.assertTrue(True)


    def test_login_invalid_user_invalid_pass(self):
        self.assertTrue(True)
    
if __name__ == '__main__':
    unittest.main()


