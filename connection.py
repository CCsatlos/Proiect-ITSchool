import pathlib
import os
from sqlalchemy import create_engine

engine = create_engine("sqlite:///D:\Python course\Proiect\sample.db")

ROOT = pathlib.Path(__file__).parent

