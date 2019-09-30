import os
import zerodata
from zerodata import *
from datetime import datetime, timedelta


class sideFunc():
    def __init__(self, dbTool, dbConn):
        self.dbTool = dbTool
        self.dbConn = dbConn

    def setCurrentUserUpdate(self, user, password):
        zerodata.LOGIN_PASSWORD_INSTA = password
        zerodata.LOGIN_USERNAME_INSTA = user
        print("+ Setting user to: {} and password to: {}".format(zerodata.LOGIN_USERNAME_INSTA, zerodata.LOGIN_PASSWORD_INSTA))

        #Update time in account
        currentTime = datetime.today()
        self.dbTool.inserttoTabel(self.dbConn, DB_UPDATE_ACCOUNT_LAST_USED, (currentTime, user,))
        print("+ Updating last time for: {} to: {}".format(user, currentTime))

    def autoSelectLogin(self):
        userList = self.runUserCheck()
        print("\n- Auto selecting login USER")

        count = 0
        currentSelect = 0
        oldestTime = datetime.strptime(str(datetime.today()), zerodata.DATETIME_MASK) #Setting current time
        for i in userList:
            lastTime = i[6]
            print("+ User: {}, last used: {}".format(i[0], lastTime))
            datetimelasttime = datetime.strptime(str(datetime.today()), zerodata.DATETIME_MASK)

            if not lastTime:
                print("+ Setting {} to oldest".format(i[0]))
                oldestTime = datetimelasttime
                currentSelect = count
                break
            else:
                datetimelasttime = datetime.strptime(lastTime, zerodata.DATETIME_MASK)

            if oldestTime >= datetimelasttime:
                #oldestTime er nyere så setter forløpig denne til eldste
                print("+ Setting {} to oldest".format(i[0]))
                oldestTime = datetimelasttime
                currentSelect = count

            count += 1

        self.setCurrentUserUpdate(userList[currentSelect][0].strip(), userList[currentSelect][1].strip())

    def runUserCheck(self):
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
                print("+ User add OK")
                self.setCurrentUserUpdate(user, password[0][0])
            return True
        else:
            if len(userList) == 1:
                print("+ One user found using: {}".format(userList[0][0]))
                self.setCurrentUserUpdate(userList[0][0].strip(), userList[0][1].strip())
                return True
            else:
                return userList

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
        userList = self.runUserCheck()
        if userList != True:
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
            self.setCurrentUserUpdate(userList[newNumber][0].strip(), userList[newNumber][1].strip())

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
