from menu import MainMenu
from classes import Employee, Task, create_the_database, create_the_database1
import pickle
import pathlib
from pathlib import Path

ROOT = pathlib.Path(__file__).parent
FOLDER = Path("D:\Phyton course\Proiect\Database")
file_path_employees = ROOT / FOLDER / "Employees.pkl"
file_path_tasks = ROOT / FOLDER / "Tasks.pkl"

emp = Employee()
tsk = Task()
the_plan = {}

create_the_database()
create_the_database1()

def planning():

    try:
        with open(file_path_employees, "rb") as fin:
            emp.employee_container = pickle.load(fin)
        with open(file_path_tasks, "rb") as fin:
            tsk.tasks_container = pickle.load(fin)

        for emp_name, whours in emp.employee_container.items():
            available_lines = whours * 60 / 6 
            for task_name, (lines, _) in tsk.tasks_container.items():  
                
                # Verificam daca sunt linii in task si spatiu productiv la angajat
                if lines > 0 and available_lines > 0:
                    allocated_lines = min(available_lines, lines)

                    # Adăugare sau actualizare în dicționarul principal
                    if task_name in the_plan:
                        the_plan[task_name][emp_name] = allocated_lines
                    else:
                        the_plan[task_name] = {emp_name : allocated_lines}

                    available_lines -= allocated_lines
                    lines -= allocated_lines
                    tsk.tasks_container[task_name] = (lines, _)

                else:
                    print("The plan was created.")
    
    except OSError as err:
        return err
    
    print (the_plan)

    
if __name__ == "__main__":

    main = MainMenu()

    create_the_database()

    main.add_option("1", "Add a new employee", lambda: emp.add_employee())
    main.add_option("2", "View the employees", lambda: emp.show_the_container())
    main.add_option("3", "Delete an employee", lambda: emp.remove_employee())
    main.add_option("4", "Change something to an employee", lambda: emp.change_something_at_employee())
    main.add_option("5", "Add a new task", lambda: tsk.add_task())
    main.add_option("6", "View the tasks", lambda: tsk.show_the_container())
    main.add_option("7", "Remove a task", lambda: tsk.remove_task())
    main.add_option("8", "Test", lambda: planning())

    main.run()
