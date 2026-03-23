import sqlite3
from . import directoryHandler

def get_con_and_cursor():
    con=sqlite3.connect(database= directoryHandler.database_path() + '/ims.db')
    cur=con.cursor()
    return cur, con