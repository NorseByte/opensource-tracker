import os
from datetime import datetime, timedelta

class sideFunc():
    def __init__(self, dbTool, dbConn, Zero):
        self.zero = Zero
        self.dbTool = dbTool
        self.dbConn = dbConn

    def setCurrentUserUpdate(self, user, password):
        self.zero.LOGIN_PASSWORD_INSTA = password
        self.zero.LOGIN_USERNAME_INSTA = user
        self.zero.printText("+ Setting user to: {} and password to: {}".format(self.zero.LOGIN_USERNAME_INSTA, self.zero.LOGIN_PASSWORD_INSTA), True)

        #Update time in account
        currentTime = datetime.today()
        self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_ACCOUNT_LAST_USED, (currentTime, user,))
        self.zero.printText("+ Updating last time for: {} to: {}".format(user, currentTime), False)

    def autoSelectLogin(self):
        userList = self.runUserCheck()
        self.zero.printText("\n- Auto selecting login user", True)
        if userList != True:
            count = 0
            currentSelect = 0
            oldestTime = datetime.strptime(str(datetime.today()), self.zero.DATETIME_MASK) #Setting current time
            for i in userList:
                lastTime = i[6]
                #Print function to list time and date, not needed.
                #self.zero.printText("+ User: {}, last used: {}".format(i[0], lastTime))
                datetimelasttime = datetime.strptime(str(datetime.today()), self.zero.DATETIME_MASK)

                if not lastTime:
                    self.zero.printText("+ {} oldest so far.".format(i[0]), False)
                    oldestTime = datetimelasttime
                    currentSelect = count
                    break
                else:
                    datetimelasttime = datetime.strptime(lastTime, self.zero.DATETIME_MASK)

                if oldestTime >= datetimelasttime:
                    #oldestTime er nyere så setter forløpig denne til eldste
                    self.zero.printText("+ {} oldest so far.".format(i[0]), False)
                    oldestTime = datetimelasttime
                    currentSelect = count

                count += 1

            self.setCurrentUserUpdate(userList[currentSelect][0].strip(), userList[currentSelect][1].strip())

    def runUserCheck(self):
        currentTime = datetime.today()
        self.zero.printText("\n- Loading INSTAGRAM user list from DB", True)
        userList = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_LOGIN_INSTA)
        if userList == 0:
            self.zero.printText("+ No user for Instagram found, please add one", True)
            user = input("+ Username: ")
            password = input("+ Password: ")
            email = input("+ Email: ")
            fullname = input("+ Fullname: ")

            self.zero.printText("+ Adding {} to DB".format(user), True)
            INSERT_DATA = (user, password, email, fullname, "instagram", currentTime)
            self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_LOGIN_INSTA, INSERT_DATA)
            password = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_LOGIN_PASSWORD_INSTA , (user,))

            if password == 0:
                #Add loop for user
                self.zero.printText("+ Not able to add user", True)

            else:
                self.zero.printText("+ User add OK", True)
                self.setCurrentUserUpdate(user, password[0][0])
            return True
        else:
            if len(userList) == 1:
                self.zero.printText("+ One user found using: {}".format(userList[0][0]), True)
                self.setCurrentUserUpdate(userList[0][0].strip(), userList[0][1].strip())
                return True
            else:
                self.zero.printText("+ User list loaded.", True)
                return userList

    def setDefValue(self, newValue, text, value_text, oneup, json):
        if newValue.isdigit():
            if oneup == False:
                if int(newValue) < 1:
                    self.zero.printText("+ Invalid input {} not changed".format(text), False)
                else:
                    self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_OPTIONS, (newValue, text))
                    value_text = newMaxFollow
                    self.zero.printText("+ {} set to: {}".format(text, value_text), True)
            if oneup == True:
                if int(newValue) > 1:
                    self.zero.printText("+ Invalid input {} not changed".format(text), False)
                else:
                    if int(newValue) < 0:
                        self.zero.printText("+ Invalid input {} not changed".format(text), False)
                    else:
                        if json == False:
                            self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_OPTIONS, (newValue, text))
                            value_text = newValue
                            self.zero.printText("+ {} set to: {}".format(text, value_text), True)
                        else:
                            value_text = newValue
                            self.zero.setupJSON(True)
                            self.zero.printText("+ {} set to: {}".format(text, value_text), True)
                            self.zero.printText("+ IF SQL CHANGE RESTART PROGRAM", True)
        else:
            self.zero.printText("+ Invalid input {} not changed".format(text), False)

    def editDefaultValue(self):
        getMaxValueFOLLOW = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, (self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT, ))[0][1]
        getMaxValueFOLLOWBY = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, (self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT, ))[0][1]
        getSurfaceScan = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, (self.zero.SURFACE_SCAN_TEXT, ))[0][1]
        getDownload = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, (self.zero.DOWNLOAD_PROFILE_INSTA_TEXT, ))[0][1]

        self.zero.printText("\n- Loading default values:", True)
        self.zero.printText("+ Max allowed follow: {}".format(getMaxValueFOLLOW), True)
        self.zero.printText("+ Max allowed follow by: {}".format(getMaxValueFOLLOWBY), True)
        self.zero.printText("+ Surface scan set to: {} (0 = OFF, 1 = ON)".format(getSurfaceScan), True)
        self.zero.printText("+ Download profile set to: {} (0 = OFF, 1 = ON)".format(getDownload), True)
        self.zero.printText("+ Detail print set to: {} (0 = OFF, 1 = ON)".format(self.zero.DETAIL_PRINT_VALUE), True)
        self.zero.printText("+ Mysql(1) - Sqlite(0): {}".format(self.zero.DB_MYSQL_ON), True)

        change = input("+ Change value? [y/N] ")

        if change.lower().strip() == "y":
            newMaxFollow = input("+ Max allowed follow: ")
            newMaxFollowBy = input("+ Max allowed followed by: ")
            newSurfaceScan = input("+ Surface scan on[1]/off[0]: ")
            newDetailPrint = input("+ Detail print on[1]/off[0]: ")
            newSavePhoto = input("+ Download profile on[1]/off[0]: ")
            newMysql = input("+ Mysql[1] - Sqlite[0]: ")

            self.setDefValue(newMaxFollow, self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT, self.zero.INSTA_MAX_FOLLOW_SCAN_VALUE, False, False)
            self.setDefValue(newMaxFollowBy, self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT, self.zero.INSTA_MAX_FOLLOW_BY_SCAN_VALUE, False, False)
            self.setDefValue(newSurfaceScan, self.zero.SURFACE_SCAN_TEXT, self.zero.SURFACE_SCAN_VALUE, True, False)
            self.setDefValue(newDetailPrint, self.zero.DETAIL_PRINT_TEXT, self.zero.DETAIL_PRINT_VALUE, True, True)
            self.setDefValue(newSavePhoto, self.zero.DOWNLOAD_PROFILE_INSTA_TEXT, self.zero.DOWNLOAD_PROFILE_INSTA_TEXT, True, False)
        else:
            self.zero.printText("+ Nothing changed.", True)

    def addLastInsta(self, update):
        lastInsta = input("+ Enter account to scrape: ")
        self.zero.printText("+ Adding {} to DB".format(lastInsta), True)
        if update == False:
            self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_OPTIONS_LASTINSTA, (lastInsta, self.zero.LAST_INSTA_TEXT))
        else:
            self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_LAST_INSTA, (lastInsta,))

        if lastInsta == 0:
            #Add loop for user
            self.zero.printText("+ Not able to add to scraper", True)
            sys.exit()

        else:
            self.zero.INSTA_USER = lastInsta
            self.zero.printText("+ Scraper enabled for: {}".format(self.zero.INSTA_USER), True)

    def lastSearch(self):
        self.zero.printText("\n- Loading last scraper for Instagram from DB", True)
        lastInsta = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, (self.zero.LAST_INSTA_TEXT, ))
        if lastInsta == 0:
            self.zero.printText("+ No last search for Instagram found", True)
            self.addLastInsta(False)

        else:
            self.zero.printText("+ Last user scraped: {}".format(lastInsta[0][1]), True)
            goon = input("+ Continue with user? [Y/n] ")

            if goon.lower().strip() == "n":
                self.addLastInsta(True)
            else:
                self.zero.INSTA_USER = lastInsta[0][1]

    def setupLogin(self):
        userList = self.runUserCheck()
        if userList != True:
            self.zero.printText("+ User list imported", True)
            count = 0
            for i in userList:
                count += 1
                self.zero.printText("[{}] {} ({}) (Last used: {})".format(count, i[0], i[3].strip(), i[6]), True)
            selectUser = input("+ Select user (1-{}): ".format(count))

            if not selectUser.isnumeric():
                self.zero.printText("+ Invalid input, #1 selected", True)
                selectUser = 1

            if int(selectUser) > count:
                self.zero.printText("+ Invalid input, #1 selected", True)
                selectUser = 1

            newNumber = int(selectUser) - 1
            self.setCurrentUserUpdate(userList[newNumber][0].strip(), userList[newNumber][1].strip())

    def countCurrentUser(self):
        userList = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_LOGIN_INSTA)
        count = 0

        if userList != 0:
            for i in userList:
                count =+ 1

        self.zero.TOTAL_USER_COUNT = count

    def loadLoginText(self):
        currentTime = datetime.today()
        self.zero.printText("\n- Loading user and password from file", True)
        for file in self.zero.USER_FILES:
            fullpath = self.zero.OP_ROOT_FOLDER_PATH_VALUE + file[0]
            if os.path.isfile(fullpath):
                self.zero.printText("+ Found: {}, extracting data".format(fullpath), True)
                with open(fullpath) as fp:
                    line = fp.readline()
                    while line:
                        newUser = line.strip().split(",")

                        if len(newUser[0]) != 0:
                            #Check if exists
                            password = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_LOGIN_PASSWORD_INSTA , (newUser[0],))

                            if password != 0:
                                self.zero.printText("+ User allready exist: {}".format(newUser[0]), False)

                            else:
                                self.zero.printText("+ User NOT found adding user: {}. ".format(newUser[0]), False)
                                INSERT_DATA = (newUser[0].strip(), newUser[1].strip(), newUser[2].strip(), newUser[3].strip(), newUser[4].strip(), currentTime)
                                self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_LOGIN_INSTA, INSERT_DATA)
                                password = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_LOGIN_PASSWORD_INSTA , (newUser[0].strip(),))

                                if password == 0:
                                    self.zero.printText("+ Not able to add user", False)
                                else:
                                    self.zero.printText("+ User add OK", False)
                        line = fp.readline()
            else:
                self.zero.printText("+ File: {} does not exist".format(fullpath), False)
