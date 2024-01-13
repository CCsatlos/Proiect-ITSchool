from datetime import datetime
import pickle
import pathlib
from pathlib import Path



ROOT = pathlib.Path(__file__).parent
FOLDER = Path("D:\Phyton course\Proiect\Database")
file_path_employees = ROOT / FOLDER / "Employees.pkl"
file_path_tasks = ROOT / FOLDER / "Tasks.pkl"



def create_the_database(file_path):
    if not file_path.exists():
        with open(file_path, "wb"):
            pass



class Employee:

    """
    The class aims to serve as a container for the dictionary of employees and manage it. 
    The methods vary from addition, modification, to deletion, depending on the need.
    """
    employee_container = []
    
    def __init__(self, name, working_hours):
        
        self.name = name
        self.working_hours = working_hours

    def find_employee(self, name):
        for employee in self.employee_container:
            if employee.name == name:
                return employee

    def add_employee(self):
        self.name = str(input("Enter the full name: ")).strip()
        self.working_hours = float(input("Enter the working hours per day: "))
        if not self.name:
            print("You didn`t enter the name.")            
        else:
            try:
                with open(file_path_employees, "rb") as fin:
                    self.employee_container = pickle.load(fin)
            except (OSError, EOFError) as err:
                print (f"Eroare: {err}")

            new_employee = Employee(self.name, self.working_hours)
            self.employee_container.append(new_employee)

            try:
                with open(file_path_employees, "wb") as fout:
                    pickle.dump(self.employee_container, fout)
            except OSError as err:
                return err

    def show_the_container(self):
        print (f"The employees are:")
        try:
            with open(file_path_employees, "rb") as fin:
                self.employee_container = pickle.load(fin)
        except (OSError, EOFError) as err:
            return err
        else:
            for employee in self.employee_container:
                print (f"{employee.name}: {employee.working_hours}" )
        
    def remove_employee(self):
        user_choice = str(input("Enter the employee`s name or 0 to exit: ")).strip()
        if user_choice == "0":
            return
        else:
            try:
                with open(file_path_employees, "rb") as fin:
                    self.employee_container = pickle.load(fin)
            
                employee_to_remove = self.find_employee(user_choice)
                if employee_to_remove:
                    self.employee_container.remove(employee_to_remove)
                else:
                    print ("No Employee fund.")
                    return
            
                with open(file_path_employees, "wb") as fout:
                    pickle.dump(self.employee_container, fout)
            except OSError as err:
                return err
            print (f"{user_choice} was deleted.")
        
    def change_something_at_employee(self):
        var1 = "working hours"
        var2 = "name"
        user_choice = str(input("Enter the name of the employee: ")).strip()
        try:
            with open(file_path_employees, "rb") as fin:
                self.employee_container = pickle.load(fin)
                the_employee = self.find_employee(user_choice)
                
            if the_employee in self.employee_container:
                next_choice = input("Enter what do you want to change: ").strip().lower()
                if next_choice == var1:
                    new_hours = float(input("Enter the hours: ").strip().lower())
                    the_employee.working_hours = new_hours
                elif next_choice == var2:
                    new_name = str(input("Enter the name: ").strip())
                    the_employee.name = new_name
                else:
                    print("Your choice isn`t valid. Please try again!")
                    return
            else:
                print("We did`nt find the employee. Please try again!")
                return
        
            with open(file_path_employees, "wb") as fout:
                pickle.dump(self.employee_container, fout)
        except OSError as err:
            return err





class Task:
    """
    The class aims to serve as a container for the dictionary of tasks and manage it. 
    The methods vary from showing available tasks, addition, modification, to deletion, 
    depending on the need.
    """
    TIME_PER_TASK = 6
    

    def __init__(self, name, lines):
        
        self.name = name
        self.lines = lines
        self.date = datetime.now()
        self.tasks_container = []

    def open_database(self):
        try:
            with open(file_path_tasks, "rb") as fin:
                self.tasks_container = pickle.load(fin)
        except (OSError, EOFError) as err:
            print (f"Eroare: {err}")

    def close_database(self):
        try:
            with open(file_path_tasks, "wb") as fout:
                pickle.dump(self.tasks_container, fout)
        except OSError as err:
            return err

    def find_task(self, name, lines):
        self.open_database()
        for task in self.tasks_container:
            if task.name == name and task.lines == lines:
                return True
            else:
                print(f"The task {name} doesn't belong to the list.")
                return False

    def check_and_add_task(self):
        self.name = str(input("Enter the task`s name: ")).strip()
        self.lines = int(input("Enter the quantity: "))
        formatted_datetime = self.date.strftime("%d.%m.%Y, %H:%M")
        
        check = self.find_task(self.name, self.lines)

        if check:
            print(f"The task {self.name} is in the list.")
            return
        else:
            self.open_database()
            
            new_task = Task(self.name, self.lines)
            new_task.date = formatted_datetime
            self.tasks_container.append(new_task)

            self.close_database()

    def show_the_container(self):
        print (f"The tasks are:")
        self.open_database()

        for task in self.tasks_container:
            print (f"{task.name} ---> lines: {task.lines}, received date: {task.date}")
    
    def remove_task(self):
        user_choice_name = str(input("Enter the task`s name you want to delete: ")).strip()
        user_choice_date = input("Enter the received date: ").strip()

        self.open_database()

        for task in self.tasks_container:

            if user_choice_name == task.name and user_choice_date == task.date:
                self.tasks_container.remove(task)
                print(f"The task {user_choice_name} was deleted.")
            else:
                print(f"No Task with name {user_choice_name}\
                    and the date {user_choice_date} found.")
                return
            
        self.close_database()
            

            


            