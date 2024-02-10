from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, delete, update
from sqlalchemy.orm import sessionmaker
from connection import engine, folder_path
from datetime import datetime
from openpyxl import Workbook, load_workbook
import os
import string


Base = declarative_base()

def create_metadata():
    Base.metadata.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()


class Employee(Base):

    """The class represents an employee. Through this class, employees can be added or deleted, 
       as well as some data related to employees can be modified."""

    __tablename__ = 'Employees'
    num_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    working_hours  = Column(Integer)
    available_lines = Column(Integer, default = 0)
    
    def __init__(self, first_name, last_name, working_hours):
        self.first_name = first_name
        self.last_name = last_name
        self.working_hours = working_hours    

    def add_employee(self):

        """Through this method, an employee can be added to the database. No arguments needed."""

        self.first_name = input("Enter the first name: ").title().strip()
        self.last_name = input("Enter the last name: ").title().strip()
        self.working_hours = float(input("Enter the working hours per day: "))
        new_employee = Employee(first_name = self.first_name,
                                last_name = self.last_name,
                                working_hours = self.working_hours)
        new_employee.available_lines = self.working_hours * 10
        session.add(new_employee)
        session.commit()

    def show_employees(self):

        """A list of all employees will be displayed."""

        list = session.query(Employee).all()
        print("=" * 30)
        print ("The list with employees.")
        print("=" * 30)
        for row in list:
            print ("ID:", row.num_id, "Name:", row.first_name, row.last_name,  "Working hours per day:", row.working_hours)
    
    def delete_item(self):

        """Through this method, an employee can be deleted from the database. No arguments needed."""

        user_input = int(input("To delete an employee, please enter the ID: "))
        check_id = session.query(Employee).get(user_input)
        if not check_id:
            print(f"We did`nt find the ID number {user_input}")
            return
        else:
            session.execute(delete(Employee).where(Employee.num_id == user_input))
            session.commit()

    def recharge_available_lines(self):

        """Through this method, the employees' available hours will be reallocated. 
           Considering that each line in the task requires 6 minutes of processing, 
           each available hour represents 10 lines in the task."""

        employees = session.query(Employee).order_by(Employee.available_lines).all()
        for employee in employees:
            hours = employee.working_hours * 10
            session.execute(update(Employee).where(Employee.num_id == employee.num_id).values(available_lines = hours))
        session.commit() 
        return

class Task(Base):

    """The class represents a task. Through this class, tasks can be added or deleted."""

    __tablename__ = 'Tasks'
    num_id = Column(Integer, primary_key=True)

    date = Column(String)
    hour = Column(String)
    name = Column(String)
    lines  = Column(Integer)
    available_lines = Column(Integer, default=lambda self: self.lines)
    
    def __init__(self, date, hour, name, lines):
        self.date = date
        self.hour = hour
        self.name = name
        self.lines = lines
        self.available_lines = lines

    def move_completed_tasks(self):

        """The method helps to archive complete tasks. The basic criterion is the number of lines left in the task. 
           If number of lines is equal to 0, then the task will be copied as a new object into the Archive class."""

        tasks = session.query(Task).filter_by(available_lines = 0).all()
        for task in tasks:
            old_task = Archive(date = task.date,
                            hour = task.hour,
                            name = task.name,
                            lines = task.lines)
            session.add(old_task)
        session.commit()

    def delete_completed_task(self):

        """Through this method, a certain task will be deleted. To be able to delete the task, you need its id number"""

        tasks = session.query(Task).filter_by(available_lines = 0).all()
        for task in tasks:
            session.execute(delete(Task).where(Task.num_id == task.num_id))
        session.commit()

    def add_task(self):

        """Through this method, a certain task will be deleted."""

        self.name = input("Enter the task`s name: ").title().strip()
        self.lines = input("Enter the number of line: ").title().strip()
        now = datetime.now()
        new_task = Task(date = now.strftime("%d/%m/%Y"),
                        hour = now.strftime("%H:%M:%S"),
                        name = self.name,
                        lines = self.lines,)
        session.add(new_task)
        session.commit()

    def show_tasks(self):

        """A list of all tasks will be displayed."""

        list = session.query(Task).all()
        print("=" * 30)
        print ("The list with tasks.")
        print("=" * 30)
        for row in list:
            print ("ID:", row.num_id, "Date:", row.date, "Hour:", row.hour, "Name:", row.name, "Nr. of lines", row.lines)

    def delete_item(self):

        """Through this method, a certain task will be deleted. To be able to delete the task, you need its id number"""

        user_input = int(input("To delete a task, please enter the ID: "))
        check_id = session.query(Task).get(user_input)
        if not check_id:
            print(f"We did`nt find the ID number {user_input}")
            return
        else:
            session.execute(delete(Task).where(Task.num_id == user_input))
            session.commit()


class Plan(Base):
     
    """This class is meant to create a time plan object. It includes methods for calculating the work 
    schedule for a working day. Also, through this class, writing to the Excel file will be performed."""

    __tablename__ = 'Plan'
    num_id = Column(Integer, primary_key=True)

    date        = Column(String)
    hour        = Column(String)
    task_name   = Column(String, ForeignKey(Task.num_id))
    users       = Column(String)
    lines       = Column(Integer)

    def __init__(self, date, hour, task_name, users, lines):
        self.date = date
        self.hour = hour
        self.task_name = task_name
        self.users = users
        self.lines = lines
        self.today = datetime.now().strftime("%d.%m.%Y")
        self.xlsx_name = f"Plan {self.today}.xlsx"
        self.file_path = os.path.join(folder_path, self.xlsx_name)

    def create_plan(self):

        """The method takes from another classes all necessary data to calculate the time plan object."""
        
        while True:
            # create two lists of available tasks and employees
            tasks = session.query(Task).order_by(Task.date.asc(), Task.available_lines.asc()).all()
            employees = session.query(Employee).order_by(Employee.available_lines.desc()).all()

            # verifying if the tasks were full assigned or if the employees` availability is at maximum capacity
            if all(task.available_lines == 0 for task in tasks) or \
               all(employee.available_lines == 0 for employee in employees):
                break
            
            for task in tasks:
                for employee in employees:
                    if task.available_lines == 0 or employee.available_lines == 0:
                        continue
                    availability = min(task.available_lines, employee.available_lines)

                    new_plan = Plan(
                        date = self.today,
                        hour = task.hour,
                        task_name = task.name,
                        users = employee.last_name,
                        lines = availability)

                    task.available_lines -= availability
                    employee.available_lines -= availability

                    session.add(new_plan)
                    session.commit()
                    Task.move_completed_tasks(Task)
                    Task.delete_completed_task(Task)
        return

    def create_workbook(self):

        if os.path.exists(self.file_path):
            print("*" * 30)
            print("The plan was created. Your data were overwrite. Please check your folder!")
            print("*" * 30)
            return
        else:
            try:
                wb = Workbook()
                wb.save(self.file_path)
            except OSError as err:
                print(err)

    def write_the_plan(self):
        
        self.create_workbook()

        plan_list = session.query(Plan).order_by(Plan.date).order_by(Plan.hour).all()

        wb = load_workbook(self.file_path)
        ws = wb.active
        ws.merge_cells('A1:E1')
        ws["A1"] = self.today
        row_idx = 2
          
        for task in plan_list:
            col_idx = 1
            for attribute in [task.date, task.hour, task.task_name, task.users, task.lines]:
                ws.cell(row = row_idx, column = col_idx, value = attribute)
                col_idx += 1
            row_idx += 1

        wb.save(self.file_path)

        for task in plan_list:
            session.execute(delete(Plan).where(Plan.num_id == task.num_id))
        session.commit()

class Archive(Base):

    """The class serves as an container for the assigned tasks. No methods are needed. """

    __tablename__ = "Archive"    
    num_id = Column(Integer, primary_key=True)

    date = Column(String)
    hour = Column(String)
    name = Column(String)
    lines  = Column(Integer)






