import os
import sqlite3
import unicodecsv as csv
import sys
from sqlite3 import Error

class dbFunc():
    def __init__(self, dbname, Zero):
        self.zero = Zero
        self.dbname = self.zero.DB_DATABASE_FOLDER + dbname
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

    def exportNode(self, conn, sql, filename):
        if os.path.exists(filename):
            print("+ File: {} exist, deleting it.".format(filename))
            os.remove(filename)

        cur = conn.cursor()
        cur.execute(sql)
        with open(filename, 'wb') as csvfile:
            print("+ Creating and writing to: {}".format(filename))
            writer = csv.writer(csvfile, encoding=self.zero.WRITE_ENCODING)
            writer.writerow([ i[0] for i in cur.description ])
            writer.writerows(cur.fetchall())

    def createDBfolder(self):
        if not os.path.exists(self.zero.DB_DATABASE_FOLDER):
            os.mkdir(self.zero.DB_DATABASE_FOLDER)

        if not os.path.exists(self.zero.DB_DATABASE_EXPORT_FOLDER):
            os.mkdir(self.zero.DB_DATABASE_EXPORT_FOLDER)

    def setDefaultValueOptions(self, conn):
        #Set max value for scan
        print("+ Setup of default values")
        getMaxValueFOLLOW = self.getValueSQL(conn, self.zero.DB_SELECT_OPTIONS, (self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT, ))
        getMaxValueFOLLOWBY = self.getValueSQL(conn, self.zero.DB_SELECT_OPTIONS, (self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT, ))

        if getMaxValueFOLLOW == 0:
            print("+ {} are NOT in database".format(self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT))
            self.inserttoTabel(conn, self.zero.DB_INSERT_OPTIONS_LASTINSTA, (self.zero.INSTA_MAX_FOLLOW_SCAN_VALUE, self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT, ))
            print("+ {} set to: {}".format(self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT, self.zero.INSTA_MAX_FOLLOW_SCAN_VALUE))

        if getMaxValueFOLLOWBY == 0:
            print("+ {} are NOT in database".format(self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT))
            self.inserttoTabel(conn, self.zero.DB_INSERT_OPTIONS_LASTINSTA, (self.zero.INSTA_MAX_FOLLOW_BY_SCAN_VALUE, self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT, ))
            print("+ {} set to: {}".format(self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT, self.zero.INSTA_MAX_FOLLOW_BY_SCAN_VALUE))

        print("+ Setup of default DONE")
