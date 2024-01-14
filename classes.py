from datetime import datetime
import pickle
import paths


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
    
    def open_database(self):
        try:
            with open(paths.file_path_employees, "rb") as fin:
                self.employee_container = pickle.load(fin)
        except (OSError, EOFError) as err:
            print (f"Eroare: {err}")
    
    def close_database(self):
        try:
            with open(paths.file_path_employees, "wb") as fout:
                pickle.dump(self.employee_container, fout)
        except OSError as err:
            return err

    def add_employee(self):
        self.name = str(input("Enter the full name: ")).strip()
        str_working_hours = str(input("Enter the working hours per day: "))

        #Handling the errors
        if not self.name or not self.working_hours:
            print("You didn`t enter the name or the working hours.")
            return
        
        self.working_hours = float(str_working_hours)
        self.open_database()
        new_employee = Employee(self.name, self.working_hours)
        self.employee_container.append(new_employee)
        self.close_database()

    def show_the_container(self):
        print (f"The employees are:")
        self.open_database()

        for employee in self.employee_container:
            print (f"{employee.name}: {employee.working_hours}" )
        
    def remove_employee(self):
        user_choice = str(input("Enter the employee`s name or 0 to exit: ")).strip()

        if user_choice == "0":
            return
        else:
            self.open_database()
            employee_to_remove = self.find_employee(user_choice)

            if employee_to_remove:
                self.employee_container.remove(employee_to_remove)
            else:
                print ("No Employee fund.")
                return

            self.close_database()
            print (f"{user_choice} was deleted.")
        
    def change_something_at_employee(self):
        var1 = "working hours"
        var2 = "name"
        user_choice = str(input("Enter the name of the employee: ")).strip()
        self.open_database()
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

        self.close_database()


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
        self.tasks_container = []

    def open_database(self):
        try:
            with open(paths.file_path_tasks, "rb") as fin:
                self.tasks_container = pickle.load(fin)
        except (OSError, EOFError) as err:
            print (f"Eroare: {err}")

    def close_database(self):
        try:
            with open(paths.file_path_tasks, "wb") as fout:
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
        task_name = str(input("Enter the task`s name: ")).strip()
        task_lines = int(input("Enter the quantity: "))
        formatted_datetime = self.date.strftime("%d.%m.%Y, %H:%M")
        
        check = self.find_task(task_name, task_lines)

        if check:
            print(f"The task {task_name} is in the list.")
            return
        else:
            self.open_database()
            
            new_task = Task(task_name, task_lines)
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
            

            
class Plan:

    """The class should create a plan for each day with the support of other classes. """

    def __init__(self):
        
        self.employees_dict = {}
        self.task_dict = {}
        self.plan_container = {}
        self.day = str(datetime.now().date())
    
    def open_databases(self):

        try:
            with open(paths.file_path_tasks, "rb") as fin:
                Task.tasks_container = pickle.load(fin)
            with open(paths.file_path_employees, "rb") as fin:
                Employee.employee_container = pickle.load(fin)
            with open(paths.file_path_plan, "rb") as fin:
                Plan.plan_container = pickle.load(fin)
        except (OSError, EOFError) as err:
            print (f"Eroare: {err}")

    def close_database(self, path: any, object: any):
        """
            The function will write the binary file. The first parameter will be 
            the path file and the second will be the object form the path in which
            you want to save the data.
        """
        
        try:
            with open(path, "wb") as fout:
                pickle.dump(object, fout)
        except OSError as err:
            return err

    def listing_employees(self):

        self.open_databases()

        for employee in Employee.employee_container:
            name = employee.name
            working_hours = employee.working_hours

            self.employees_dict[name] = working_hours
        
    def listing_tasks(self):

        self.open_databases()

        for task in Task.tasks_container:
            task_name = task.name
            task_lines = task.lines
        
        self.task_dict[task_name] = task_lines
    
    def create_the_plan(self):

        self.listing_employees()
        self.listing_tasks()
        self.open_databases()

        for task_name, lines in self.task_dict.items():
            if self.day not in self.plan_container.keys():
                self.plan_container[self.day] = {}
            
                for emp_name, whours in self.employees_dict.items():
                    available_lines = whours * 60 / 6
                    allocated_lines = min(available_lines, lines)

                    if task_name not in self.plan_container[self.day]:
                        self.plan_container[self.day][task_name] = []
                    
                    self.plan_container[self.day][task_name].append((emp_name, allocated_lines))
                self.close_database(paths.file_path_plan ,self.plan_container)
            else:
                print(f"The plan was created.")
                return
            
        self.close_database(paths.file_path_tasks, Task.tasks_container)
        self.close_database(paths.file_path_employees, Employee.employee_container)
        print(self.plan_container)

    def show_the_plan(self):
        self.open_databases()
        for day, task_name in self.plan_container.items():
            print (f"The day: {day} ----> Tasks: {task_name}")
    
