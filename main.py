from menu import MainMenu
from classes import Employee, Task, Plan, create_the_database
import paths

emp = Employee("Test", 0)
tsk = Task("Test", 0)
plan = Plan()

create_the_database(paths.file_path_employees)
create_the_database(paths.file_path_tasks)
create_the_database(paths.file_path_plan)
    
if __name__ == "__main__":

    main = MainMenu()

    main.add_option("1", "Add a new employee", lambda: emp.add_employee())
    main.add_option("2", "View the employees", lambda: emp.show_the_container())
    main.add_option("3", "Delete an employee", lambda: emp.remove_employee())
    main.add_option("4", "Change something to an employee", lambda: emp.change_something_at_employee())
    main.add_option("5", "Add a new task", lambda: tsk.check_and_add_task())
    main.add_option("6", "View the tasks", lambda: tsk.show_the_container())
    main.add_option("7", "Remove a task", lambda: tsk.remove_task())
    main.add_option("8", "Create the plan", lambda: plan.create_the_plan())
    main.add_option("9", "Show the plan", lambda: plan.show_the_plan())

    main.run()
