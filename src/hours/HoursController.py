
from PyQt5 import QtWidgets
from src.RUPaid.Crypt import Hashing
from src.employee.EmployeeView import EmployeeView
from src.RUPaid.DatabaseConnection import DBConnection
from src.hours.HoursView import HoursView
from PyQt5.QtWidgets import QApplication
import sys
from src.RUPaid.DatabaseConnection import DBConnection
from PyQt5.QtCore import *

from datetime import datetime, date
from datetime import timedelta
import calendar

class HoursController:
    def __init__(self, user_id, employee_id):
        self.user_id = user_id
        self.employee_id = employee_id
        
        self.db_connection = DBConnection()
        self.ui = HoursView(self)
        self.ui.show()
        self.populate_table()

    def get_date_ranges(self):
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end
    
    def get_all_hours(self, start, end):
        hours = self.db_connection.get_employees_hours(start, end, self.employee_id)
        hours = hours.fetchall()
        return hours
            
    def populate_table(self):
        start, end = self.get_date_ranges()
        start_day = start.day
        end_day = end.day
        month_range = calendar.monthrange(datetime.now().year, 4)
        end_of_month = month_range[1]
        print(end_of_month)
        monday = start_day
        tuesday = monday + 1 if monday + 1 <= end_of_month else 1
        wednesday = tuesday + 1 if tuesday + 1 <= end_of_month else 1
        thursday = wednesday + 1 if wednesday + 1 <= end_of_month else 1
        friday = thursday + 1 if thursday + 1 <= end_of_month else 1
        saturday = friday + 1 if friday + 1 <= end_of_month else 1
        sunday = saturday + 1 if saturday + 1 <= end_of_month else 1
        
        
        hours = self.get_all_hours(start, end)
        for row in hours:
            print(row)
            temp_start_day = row[1].day
            
            temp_start_time = row[1].time()
            temp_end_time = row[2].time()
            temp_hours_worked = row[3].time()
            if(temp_start_day == monday):
                self.ui.hoursTable.setItem(1,0, QtWidgets.QTableWidgetItem("Clock In Time"))
                self.ui.hoursTable.setItem(2,0, QtWidgets.QTableWidgetItem(str(temp_start_time)))
                self.ui.hoursTable.setItem(3,0, QtWidgets.QTableWidgetItem("Clock Out Time"))
                self.ui.hoursTable.setItem(4,0, QtWidgets.QTableWidgetItem(str(temp_end_time)))
                self.ui.hoursTable.setItem(5,0, QtWidgets.QTableWidgetItem("Hours Worked"))
                self.ui.hoursTable.setItem(6,0, QtWidgets.QTableWidgetItem(str(temp_hours_worked)))
            elif(temp_start_day == tuesday):
                self.ui.hoursTable.setItem(1,1, QtWidgets.QTableWidgetItem("Clock In Time"))
                self.ui.hoursTable.setItem(2,1, QtWidgets.QTableWidgetItem(str(temp_start_time)))
                self.ui.hoursTable.setItem(3,1, QtWidgets.QTableWidgetItem("Clock Out Time"))
                self.ui.hoursTable.setItem(4,1, QtWidgets.QTableWidgetItem(str(temp_end_time)))
                self.ui.hoursTable.setItem(5,1, QtWidgets.QTableWidgetItem("Hours Worked"))
                self.ui.hoursTable.setItem(6,1, QtWidgets.QTableWidgetItem(str(temp_hours_worked)))
            elif(temp_start_day == wednesday):
                self.ui.hoursTable.setItem(1,2, QtWidgets.QTableWidgetItem("Clock In Time"))
                self.ui.hoursTable.setItem(2,2, QtWidgets.QTableWidgetItem(str(temp_start_time)))
                self.ui.hoursTable.setItem(3,2, QtWidgets.QTableWidgetItem("Clock Out Time"))
                self.ui.hoursTable.setItem(4,2, QtWidgets.QTableWidgetItem(str(temp_end_time)))
                self.ui.hoursTable.setItem(5,2, QtWidgets.QTableWidgetItem("Hours Worked"))
                self.ui.hoursTable.setItem(6,2, QtWidgets.QTableWidgetItem(str(temp_hours_worked)))
            elif(temp_start_day == thursday):
                self.ui.hoursTable.setItem(1,3, QtWidgets.QTableWidgetItem("Clock In Time"))
                self.ui.hoursTable.setItem(2,3, QtWidgets.QTableWidgetItem(str(temp_start_time)))
                self.ui.hoursTable.setItem(3,3, QtWidgets.QTableWidgetItem("Clock Out Time"))
                self.ui.hoursTable.setItem(4,3, QtWidgets.QTableWidgetItem(str(temp_end_time)))
                self.ui.hoursTable.setItem(5,3, QtWidgets.QTableWidgetItem("Hours Worked"))
                self.ui.hoursTable.setItem(6,3, QtWidgets.QTableWidgetItem(str(temp_hours_worked)))
            elif(temp_start_day == friday):
                self.ui.hoursTable.setItem(1,4, QtWidgets.QTableWidgetItem("Clock In Time"))
                self.ui.hoursTable.setItem(2,4, QtWidgets.QTableWidgetItem(str(temp_start_time)))
                self.ui.hoursTable.setItem(3,4, QtWidgets.QTableWidgetItem("Clock Out Time"))
                self.ui.hoursTable.setItem(4,4, QtWidgets.QTableWidgetItem(str(temp_end_time)))
                self.ui.hoursTable.setItem(5,4, QtWidgets.QTableWidgetItem("Hours Worked"))
                self.ui.hoursTable.setItem(6,4, QtWidgets.QTableWidgetItem(str(temp_hours_worked)))
            elif(temp_start_day == saturday):
                self.ui.hoursTable.setItem(1,5, QtWidgets.QTableWidgetItem("Clock In Time"))
                self.ui.hoursTable.setItem(2,5, QtWidgets.QTableWidgetItem(str(temp_start_time)))
                self.ui.hoursTable.setItem(3,5, QtWidgets.QTableWidgetItem("Clock Out Time"))
                self.ui.hoursTable.setItem(4,5, QtWidgets.QTableWidgetItem(str(temp_end_time)))
                self.ui.hoursTable.setItem(5,5, QtWidgets.QTableWidgetItem("Hours Worked"))
                self.ui.hoursTable.setItem(6,5, QtWidgets.QTableWidgetItem(str(temp_hours_worked)))
            elif(temp_start_day == sunday):
                self.ui.hoursTable.setItem(1,6, QtWidgets.QTableWidgetItem("Clock In Time"))
                self.ui.hoursTable.setItem(2,6, QtWidgets.QTableWidgetItem(str(temp_start_time)))
                self.ui.hoursTable.setItem(3,6, QtWidgets.QTableWidgetItem("Clock Out Time"))
                self.ui.hoursTable.setItem(4,6, QtWidgets.QTableWidgetItem(str(temp_end_time)))
                self.ui.hoursTable.setItem(5,6, QtWidgets.QTableWidgetItem("Hours Worked"))
                self.ui.hoursTable.setItem(6,6, QtWidgets.QTableWidgetItem(str(temp_hours_worked)))
'''
app = QApplication(sys.argv)
t = HoursController(8, 50)

t.ui.show()
sys.exit(app.exec_())
'''






