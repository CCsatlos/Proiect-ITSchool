from menu import MainMenu
from classes import Employee, Task, Plan
import database as db

emp = Employee("Test", "Test 2", 0)
tsk = Task("Test", 0)
plan = Plan()

db.create_table(db.conn, db.CREATE_EMPLOYEES_TABLE)
db.create_table(db.conn, db.CREATE_TASK_TABLE)

if __name__ == "__main__":

    main = MainMenu()

    main.add_option("1", "Add a new employee", lambda: emp.add_employee())
    main.add_option("2", "View the employees", lambda: emp.show_the_container())
    main.add_option("3", "Delete an employee", lambda: emp.remove_employee())
    main.add_option("4", "Change something to an employee", lambda: emp.change_something_at_employee()) # not implemented
    main.add_option("5", "Add a new task", lambda: tsk.check_and_add_task())
    main.add_option("6", "View the tasks", lambda: tsk.show_the_container()) 
    main.add_option("7", "Remove a task", lambda: tsk.remove_task()) 
    main.add_option("8", "Create the plan", lambda: plan.create_daily_plan()) # not implemented

    main.run()
