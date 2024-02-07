import classes
from menu import MainMenu

classes.create_metadata()

emp = classes.Employee("first name", "last name", 0)
tsk = classes.Task("date", "hours", "name", 0)
pln = classes.Plan("date", "task_name", "users", 0)

if __name__ == "__main__":
    main = MainMenu()
    main.add_option("1", "Add a new employee", lambda: classes.Employee.add_employee(emp))
    main.add_option("2", "View the employees", lambda: classes.Employee.show_employees(emp))
    main.add_option("3", "Delete an employee", lambda: classes.Employee.delete_item(emp))
    main.add_option("4", "Add a task", lambda: classes.Task.add_task(tsk))
    main.add_option("5", "View the tasks", lambda: classes.Task.show_tasks(tsk))
    main.add_option("6", "Delete a task", lambda: classes.Task.delete_item(tsk))
    main.add_option("7", "Create a plan", lambda: classes.Plan.create_plan(pln))
    main.add_option("8", "Recharge available lines for employees", lambda: classes.Employee.recharge_available_lines(emp))
    main.run()
    
