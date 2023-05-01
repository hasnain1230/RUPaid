from src.employee.EmployeeController import *
import unittest

class EmployeeControllerTest(unittest.TestCase):
    def test_init(self):
        employee_data_test=["test_company",1,30,"test_first_name","test_last_name",""]

        controller = EmployeeController(employee_data_test)

    def test_save_information(self):

        return
    
    def test_clock_in(self,controller):
        self.controller.clock_in()

    
    def test_clock_out(self):
        return
    
    def test_get_time_checked_in(self,userid):
        return
    
    def test_check_password(self,password):
        return
    
    def test_update_password(self,password):
        return
    
    def test_logout(self):
        return


if __name__ == '__main__':
    unittest.main()


