Task Planer

Inspired by common situations encountered when working in teams in various professional 
environments, the program is designed to reduce the time required for allocating tasks 
to employees by the administrator when a large number of employees and tasks are involved.
The program is based on CLI. 
The menu is a CLI type. To query the database, it is recommended to use a specific tool 
for SQLite, such as DB Browser. Partially, querying can also be done through the CLI menu.


Short brief explanation 

  Employee Management:
        Users can add new employees to the system by providing their full name and working hours per day.
        Existing employees can be deleted from the system if needed.
        The system allows users to view a list of all employees currently stored.

  Task Management:
        Users can add new tasks to the system by specifying the task name and the number of lines required.
        Existing tasks can be deleted from the system if they are no longer needed.
        Users can view a list of all tasks currently stored in the system.

  Time Planning:
        The system automatically updates the status of tasks to "completed" when all required lines have been assigned.
        Users can create a time plan based on the available employees and tasks. The plan allocates tasks to employees based
        on their availability and the number of lines required for each task.
        The time plan can be exported to an Excel file for further reference.
