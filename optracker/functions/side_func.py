import os
import zerodata
from zerodata import *


class sideFunc():
    def __init__(self, dbTool, dbConn):
        self.dbTool = dbTool
        self.dbConn = dbConn

    def addLastInsta(self, update):
        lastInsta = input("+ Enter account to scrape: ")
        print("+ Adding {} to DB".format(lastInsta))
        if update == False:
            self.dbTool.inserttoTabel(self.dbConn, DB_INSERT_OPTIONS_LASTINSTA, ("last_insta", lastInsta))
        else:
            self.dbTool.inserttoTabel(self.dbConn, DB_UPDATE_LAST_INSTA, (lastInsta,))

        if lastInsta == 0:
            #Add loop for user
            print("+ Not able to add to scraper")
            sys.exit()

        else:
            zerodata.INSTA_USER = lastInsta
            print("+ Scraper enabled for: {}".format(zerodata.INSTA_USER))

    def lastSearch(self):
        print("\n- Loading last scraper for Instagram from DB")
        lastInsta = self.dbTool.getValueSQL(self.dbConn, DB_SELECT_OPTIONS, ("last_insta", ))
        if lastInsta == 0:
            print("+ No last search for Instagram found")
            self.addLastInsta(False)

        else:
            print("+ Last user scraped: {}".format(lastInsta[0][1]))
            goon = input("+ Continue with user? (D:Y, Y/N) ")

            if goon.lower().strip() == "n":
                self.addLastInsta(True)
            else:
                zerodata.INSTA_USER = lastInsta[0][1]

    def setupLogin(self):
        print("\n- Loading INSTAGRAM user list from DB")
        userList = self.dbTool.getValueSQLnoinput(self.dbConn, DB_SELECT_LOGIN_INSTA)
        if userList == 0:
            print("+ No user for Instagram found, please add one")
            user = input("+ Username: ")
            password = input("+ Password: ")
            email = input("+ Email: ")
            fullname = input("+ Fullname: ")

            print("+ Adding {} to DB".format(user))
            INSERT_DATA = (user, password, email, fullname, "instagram")
            self.dbTool.inserttoTabel(self.dbConn, DB_INSERT_LOGIN_INSTA, INSERT_DATA)
            password = self.dbTool.getValueSQL(self.dbConn, DB_SELECT_LOGIN_PASSWORD_INSTA , (user,))

            if password == 0:
                #Add loop for user
                print("+ Not able to add user")

            else:
                zerodata.LOGIN_PASSWORD_INSTA = password[0][0]
                zerodata.LOGIN_USERNAME_INSTA = user
                print("+ User add OK")
                print("+ Setting user to: {} and password to: {}".format(password[0][0], user))

        else:
            if len(userList) == 1:
                print("+ One user found using: {}".format(userList[0][0]))
                zerodata.LOGIN_PASSWORD_INSTA = userList[0][1].strip()
                zerodata.LOGIN_USERNAME_INSTA = userList[0][0].strip()
                print("+ Setting user to: {} and password to: {}".format(LOGIN_USERNAME_INSTA, LOGIN_PASSWORD_INSTA))
            else:
                print("+ User list imported")
                count = 0
                for i in userList:
                    count += 1
                    print("[{}] {} ({})".format(count, i[0], i[3]))
                selectUser = input("+ Select user (1-{}): ".format(count))

                if not selectUser.isnumeric():
                    print("+ Invalid input, #1 selected")
                    selectUser = 1

                if int(selectUser) > count:
                    print("+ Invalid input, #1 selected")
                    selectUser = 1

                newNumber = int(selectUser) - 1

                zerodata.LOGIN_PASSWORD_INSTA = userList[newNumber][1].strip()
                zerodata.LOGIN_USERNAME_INSTA = userList[newNumber][0].strip()
                print("+ Setting user to: {} and password to: {}".format(zerodata.LOGIN_USERNAME_INSTA, zerodata.LOGIN_PASSWORD_INSTA))


    def loadLoginText(self):
        print("\n- Loading user and password from file")
        for file in USER_FILES:
            if os.path.isfile(file[0]):
                print("+ Found: {}, extracting data".format(file[0]))
                with open(file[0]) as fp:
                    line = fp.readline()
                    while line:
                        newUser = line.strip().split(",")

                        if len(newUser[0]) != 0:
                            #Check if exists
                            password = self.dbTool.getValueSQL(self.dbConn, DB_SELECT_LOGIN_PASSWORD_INSTA , (newUser[0],))

                            if password != 0:
                                print("+ User allready exist: {}".format(newUser[0]))

                            else:
                                print("+ User NOT found adding user: {}. ".format(newUser[0]), end = " ")
                                INSERT_DATA = (newUser[0], newUser[1], newUser[2], newUser[3])
                                self.dbTool.inserttoTabel(self.dbConn, DB_INSERT_LOGIN_INSTA, INSERT_DATA)
                                password = self.dbTool.getValueSQL(self.dbConn, DB_SELECT_LOGIN_PASSWORD_INSTA , (newUser[0],))

                                if password == 0:
                                    print("(Not able to add user)")
                                    sys.exit()
                                else:
                                    print("(User add OK)")
                        line = fp.readline()
            else:
                print("+ File: {} does not exist".format(file[0]))
