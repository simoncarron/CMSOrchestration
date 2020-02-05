import xml.etree.ElementTree as ET
import sqlite3
import itertools
from flask import Flask, g, session

import config as settings

import os

app = Flask(__name__)

def createDataBase():
    if not os.path.exists(settings.DATABASE_FOLDER_NAME):
        os.makedirs(settings.DATABASE_FOLDER_NAME)

    database = os.path.join(os.getcwd(), settings.DATABASE_FOLDER_NAME, settings.DATABASE_NAME)
    conn = sqlite3.connect(database)

    schema = os.path.join(os.getcwd(), settings.DATABASE_FOLDER_NAME, settings.DATABASE_SCHEMA)

    with app.open_resource(schema, mode='r') as f:
        conn.cursor().executescript(f.read())

