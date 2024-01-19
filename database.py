import paths
import sqlite3

CREATE_EMPLOYEES_TABLE = """CREATE TABLE IF NOT EXISTS "employee" (
            "id"             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "first_name"     TEXT NOT NULL,
            "last_name"      TEXT NOT NULL,
            "working_hours"  FLOAT NOT NULL
)"""

CREATE_TASK_TABLE = """CREATE TABLE IF NOT EXISTS "tasks" (
            "id"             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "name"           TEXT NOT NULL,
            "date"           TEXT NOT NULL,
            "lines"          INT NOT NULL
)"""

conn = sqlite3.connect(paths.db_file_path)

def create_table(connection, the_table):
    with connection:
        connection.execute(the_table)

def insert_employee(connection, first_name, last_name, working_hours):
    with connection:
        connection.execute("""INSERT INTO "employee"
            (first_name, last_name, working_hours)
            VALUES
            (?, ?, ?)""", (first_name, last_name, working_hours))

def insert_task(connection, name, date, lines):
    with connection:
        connection.execute("""INSERT INTO "tasks"
            (name, date, lines)
            VALUES
            (?, ?, ?)""", (name, date, lines))
             
def select_employee(connection, first_name, last_name):
    
    with connection:
        connection.execute("""SELECT * FROM "employee"
                           WHERE 
                           first_name = ?,
                           last_name = ? 
                            """), (first_name, last_name)

def show_tasks(connection):

    with connection:
        list = connection.execute(""" SELECT
                       name,
                       date,
                       lines
                       FROM
                       tasks
                        """)
        tasks = list.fetchall()

        for task in tasks:
            print (f"{task[0]}   {task[1]} --->  {task[2]}")

def show_employees(connection):

    with connection:
        list = connection.execute(""" SELECT
                       id,
                       first_name,
                       working_hours
                       FROM
                       employee
                        """)
        employees = list.fetchall()
        for employee in employees:
            print (f"{employee[0]}   {employee[1]}   {employee[2]}")

def remove_employee(connection, first_name, last_name):
    with connection:
        list = connection.execute("""DELETE FROM "employee"
                           WHERE
                           first_name = ? AND
                           last_name = ?
                            """, (first_name, last_name))
        
        if list.rowcount == 0:
            print(f"No employee with the name {first_name} {last_name} found.")
        else:
            print(f"{first_name} {last_name} was deleted.")
            return

def remove_task(connection, name, date):
    with connection:
        list = connection.execute("""DELETE FROM "tasks"
                           WHERE
                           name = ? AND
                           date = ? 
                            """, (name, date))
        
        if list.rowcount == 0:
            print(f"No task with the name {name} and date {date} found.")
        else:
            print(f"{name} from {date} was deleted.")
            return

def select_task(connection, name, lines):
    
    with connection:
        object = connection.execute("""SELECT * FROM "tasks"
                           WHERE 
                           name = ? AND
                           lines = ? 
                            """, (name, lines))

        task = object.fetchone()
        if task == None:
            return False
        else:
            return True