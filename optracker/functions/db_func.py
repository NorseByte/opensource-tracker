import os
import sqlite3
from sqlite3 import Error
from zerodata import *


class dbFunc():
    def __init__(self, dbname):
        self.dbname = DB_DATABASE_FOLDER + dbname
        self.createDBfolder()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbname)
        except Error as e:
                print(e)
        return conn

    def createTabels(self, conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def inserttoTabel(self, conn, sql, task):
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

    def getValueSQL(self, conn, sql, task):
        cur = conn.cursor()
        cur.execute(sql, task)
        rows = cur.fetchall()

        if rows:
            return rows
        else:
            return 0

    def getValueSQLnoinput(self, conn, sql):
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        if rows:
            return rows
        else:
            return 0

    def createDBfolder(self):
        if not os.path.exists(DB_DATABASE_FOLDER):
            os.mkdir(DB_DATABASE_FOLDER)
