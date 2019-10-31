import os
import sqlite3
import unicodecsv as csv
import sys
import mysql.connector
from sqlite3 import Error



class dbFunc():
    def __init__(self, dbname, Zero):
        self.zero = Zero
        self.dbname = self.zero.DB_DATABASE_FOLDER + dbname
        self.createDBfolder()

    def create_connection(self):
        conn = None
        if self.zero.DB_MYSQL_ON == 0:
            try:
                self.zero.printText("+ Connection to: SQLite", True)
                conn = sqlite3.connect(self.dbname)
            except Error as e:
                print(e)
        else:
            try:
                self.zero.printText("+ Connection to: MySQL", True)
                conn = mysql.connector.connect(host= self.zero.DB_MYSQL, database=self.zero.DB_MYSQL_DATABASE, user=self.zero.DB_MYSQL_USER, passwd=self.zero.DB_MYSQL_PASSWORD, charset=self.zero.DB_MYSQL_CHARSET, collation=self.zero.DB_MYSQL_COLLATION)
            except Exception as e:
                print(e)

        self.zero.printText("+ Connection to DB done.", False)
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

    def inserttoTabelMulti(self, conn, sql, task):
        if self.zero.DB_MYSQL_ON == 1:
            c = conn.cursor(buffered=True)
            results = c.execute(sql, task, multi=True)
            for cur in results:
                    if cur.with_rows:
                        data = cur.fetchall()
            conn.commit()

        else:
            newSQL = sql.replace("?", "'%s'")
            exeSQL = (newSQL % task)
            multi = exeSQL.split(";")
            lenM = len(multi)
            counter = 0

            cur = conn.cursor()
            for i in multi:
                counter += 1
                if counter != lenM:
                    cur.execute(i)

            data = cur.fetchall()
            conn.commit()

        if data:
            return data
        else:
            return 0

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

    def setDefaultValue(self, conn, text, value):
        getValue = self.getValueSQL(conn, self.zero.DB_SELECT_OPTIONS, (text, ))
        if getValue == 0:
            self.zero.printText("+ {} are NOT in database".format(text), True)
            self.inserttoTabel(conn, self.zero.DB_INSERT_OPTIONS_LASTINSTA, (value, text, ))
            self.zero.printText("+ {} set to: {}".format(text, value), True)
        else:
            self.zero.printText("+ {} in database, value set to: {}".format(text, getValue[0][1]), False)

    def setDefaultValueOptions(self, conn):
        #Set max value for scan
        print("+ Setup of default values")
        self.setDefaultValue(conn, self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT, self.zero.INSTA_MAX_FOLLOW_SCAN_VALUE)
        self.setDefaultValue(conn, self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT, self.zero.INSTA_MAX_FOLLOW_BY_SCAN_VALUE)
        self.setDefaultValue(conn, self.zero.SURFACE_SCAN_TEXT, self.zero.SURFACE_SCAN_VALUE)
        self.setDefaultValue(conn, self.zero.DOWNLOAD_PROFILE_INSTA_TEXT, self.zero.DOWNLOAD_PROFILE_INSTA_VALUE)
        self.setDefaultValue(conn, self.zero.FACEREC_ON_TEXT, self.zero.FACEREC_ON_VALUE)
        self.zero.printText("+ Setup of default DONE", False)
