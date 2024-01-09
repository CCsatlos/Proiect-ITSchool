from datetime import datetime
import pickle
import pathlib
from pathlib import Path



ROOT = pathlib.Path(__file__).parent
FOLDER = Path("D:\Phyton course\Proiect\Database")
file_path_employees = ROOT / FOLDER / "Employees.pkl"
file_path_tasks = ROOT / FOLDER / "Tasks.pkl"



def create_the_database():
    if not file_path_employees.exists():
        with open(file_path_employees, "wb"):
            pass

def create_the_database1():
    if not file_path_tasks.exists():
        with open(file_path_tasks, "wb"):
            pass



class Employee:

    """
    The class aims to serve as a container for the dictionary of employees and manage it. 
    The methods vary from addition, modification, to deletion, depending on the need.
    """

    def __init__(self):
        self.employee_container = {}
        
    def add_employee(self):
        name = str(input("Enter the full name: ")).strip()
        working_hours = float(input("Enter the working hours per day: "))
        if not name:
            print("You didn`t enter the name.")            
        else:
            try:
                with open(file_path_employees, "rb") as fin:
                    self.employee_container = pickle.load(fin)
            except (OSError, EOFError) as err:
                print (f"Eroare: {err}")

            self.employee_container[name] = working_hours

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
        except OSError as err:
            return err
        else:
            for key, value in self.employee_container.items():
                print (f"{key} ----> {value}" )
        
    def remove_employee(self):
        user_choice = str(input("Enter the employee`s name or 0 to exit: ")).strip()
        if user_choice == "0":
            return
        else:
            try:
                with open(file_path_employees, "rb") as fin:
                    self.employee_container = pickle.load(fin)
            
                self.employee_container.pop(user_choice)
            
                with open(file_path_employees, "wb") as fout:
                    pickle.dump(self.employee_container, fout)
            except OSError as err:
                return err
            print (f"{user_choice} was deleted.")
        
    def change_something_at_employee(self):
        var1 = "Working hours"
        var2 = "Name"
        user_choice = str(input("Enter the name of the employee: ")).strip()
        try:
            with open(file_path_employees, "rb") as fin:
                self.employee_container = pickle.load(fin)
        
            if user_choice in self.employee_container:
                next_choice = input("What do you want to change? ").lower().strip()

                if next_choice == var1.lower():
                    new_working_hours = str(input("Enter the working hours for the employee: "))
                    self.employee_container[user_choice] = new_working_hours
                elif next_choice == var2.lower():
                    the_new_name = str(input("Enter the new name: ")).strip()
                    the_hours = float(input("Enter the working hours: "))
                    self.employee_container.pop(user_choice)
                    self.employee_container[the_new_name] = the_hours
                else:
                    print("Your choice doesn`t match. Please try again!")
        
            with open(file_path_employees, "wb") as fout:
                pickle.dump(self.employee_container, fout)
        except OSError as err:
            return err

    def get_avl_whours(self):
        total = 0
        for hours in self.employee_container.values():
            total += hours
        return total    

class Task:
    """
    The class aims to serve as a container for the dictionary of tasks and manage it. 
    The methods vary from showing available tasks, addition, modification, to deletion, 
    depending on the need.
    """
    TIME_PER_TASK = 6

    def __init__(self):
        self.tasks_container = {}   

    def add_task(self):
        name = str(input("Enter the task`s name: ")).strip()
        lines = int(input("Enter the quantity: "))
        date = datetime.now()
        formatted_datetime = date.strftime("%d.%m.%Y, %H:%M")
        if name in self.tasks_container:
            print(f"you received this task on ...")
        else:
            try:
                with open(file_path_tasks, "rb") as fin:
                    self.tasks_container = pickle.load(fin)
            except (OSError, EOFError) as err:
                print (f"Eroare: {err}")
            
            self.tasks_container[name] = [lines, formatted_datetime]

            try:
                with open(file_path_tasks, "wb") as fout:
                    pickle.dump(self.tasks_container, fout)
            except OSError as err:
                return err
    
    def show_the_container(self):
        print (f"The tasks are:")
        try:
            with open(file_path_tasks, "rb") as fin:
                self.tasks_container = pickle.load(fin)
        except OSError as err:
            return err
        else:
            for key, (lines, date) in self.tasks_container.items():
                print (F"{key} ---> lines: {lines}, received date: {date}")
    
    def remove_task(self):
        user_choice_name = str(input("Enter the task`s name you want to delete: "))
        user_choice_date = input("Enter the received date: ")

        try: 
            with open(file_path_tasks, "rb") as fin:
                self.tasks_container = pickle.load(fin)

            if user_choice_name in self.tasks_container.keys() and \
                user_choice_date in self.tasks_container[user_choice_name]:
                self.tasks_container.pop(user_choice_name)
                print(f"The task {user_choice_name} was deleted.")
            else:
                print(f"No Task with name {user_choice_name}\
                    and the date {user_choice_date} found.")
            
            with open(file_path_tasks, "wb") as fout:
                pickle.dump(self.tasks_container, fout)
        
        except OSError as err:
            return err
            
    def get_avl_lines(self):
        total = 0
        for quantity, _ in self.tasks_container.values():
            total += quantity
        return total
            


            