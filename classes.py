from datetime import datetime
import pickle
import paths
import database as db
class Employee:

    """
    The class aims to serve as a container for the dictionary of employees and manage it. 
    The methods vary from addition, modification, to deletion, depending on the need.
    """
    
    def __init__(self, f_name, l_name, working_hours):
        
        self.first_name = f_name
        self.last_name = l_name
        self.working_hours = working_hours

    def add_employee(self):
        self.first_name = input("Enter the first name: ").strip()
        self.last_name = input("Enter the last name: ").strip()
        self.working_hours = float(input("Enter the working hours per day: "))

        db.insert_employee(db.conn, self.first_name, self.last_name, self.working_hours)

    def show_the_container(self):
        print (f"The employees are:")
        db.show_employees(db.conn)

    def remove_employee(self):

        first_name = input("Enter the employee`s first_name or 0 to exit: ").strip()
        last_name = input("Enter the employee`s last_name or 0 to exit: ").strip()

        db.remove_employee(db.conn, first_name, last_name)
        
    def change_something_at_employee(self):
        pass


class Task:
    """
    The class aims to serve as a container for the dictionary of tasks and manage it. 
    The methods vary from showing available tasks, addition, modification, to deletion, 
    depending on the need.
    """

    def __init__(self, name, lines):
        
        self.name = name
        self.lines = lines
        self.date = datetime.now()

    def check_and_add_task(self):
        self.name = str(input("Enter the task`s name: ")).strip()
        self.lines = int(input("Enter the quantity: "))
        formatted_datetime = self.date.strftime("%d.%m.%Y, %H:%M")
        
        task_exist = db.select_task(db.conn, self.name, self.lines)

        if task_exist:
            print(f"The task {self.name} is already in the list.")
            return
        else:
            db.insert_task(db.conn, self.name, formatted_datetime, self.lines)

    def show_the_container(self):
        print (f"The tasks are:")
        db.show_tasks(db.conn)
    
    def remove_task(self):

        user_choice_name = str(input("Enter the task`s name you want to delete: ")).strip()
        user_choice_date = input("Enter the received date: ").strip()

        db.remove_task(db.conn, user_choice_name, user_choice_date)
            
            
class Plan:

    """The class should create a plan for each day with the support of other classes. """

    def __init__(self):
        
        self.day = str(datetime.now().date())

    def create_daily_plan():
        pass
    
    def show_plan():
        pass


    
