import pathlib
from pathlib import Path

ROOT = pathlib.Path(__file__).parent
FOLDER = Path("D:\Phyton course\Proiect\Database")
file_path_employees = ROOT / FOLDER / "Employees.pkl"
file_path_tasks = ROOT / FOLDER / "Tasks.pkl"
file_path_plan = ROOT / FOLDER / "Plan.pkl"