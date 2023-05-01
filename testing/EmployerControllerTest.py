import sys
sys.path.append('src')

from src.employer.EmployerController import *
import unittest

class EmployerControllerTest(unittest.TestCase):

    def test_init(self):
        employee_data_test=["test_company",30,30,
                            "test_first_name","test_last_name","employer",30,"test_occupation","test_email","test_account_number","test_routing_number"]

        self.employeeController = EmployerController.EmployerController(employee_data_test)

    def get_connection(self):
        pass

    #def test_save_information(self):
#
 #       return
    
    def test_clock_in(self):
        self.employeeController.clock_in()
        pass

    
    def test_clock_out(self):
        pass
    
    def test_get_time_checked_in(self,userid):
        pass
    
    def test_check_password(self,password):
        return
    
    def test_update_password(self,password):
        return
    
    def test_logout(self):
        return


if __name__ == '__main__':
    unittest.main()


