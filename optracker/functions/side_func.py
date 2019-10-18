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
        print("+ Setting user to: {} and password to: {}".format(self.zero.LOGIN_USERNAME_INSTA, self.zero.LOGIN_PASSWORD_INSTA))

        #Update time in account
        currentTime = datetime.today()
        self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_ACCOUNT_LAST_USED, (currentTime, user,))
        print("+ Updating last time for: {} to: {}".format(user, currentTime))

    def autoSelectLogin(self):
        userList = self.runUserCheck()
        print("\n- Auto selecting login user")
        if userList != True:
            count = 0
            currentSelect = 0
            oldestTime = datetime.strptime(str(datetime.today()), self.zero.DATETIME_MASK) #Setting current time
            for i in userList:
                lastTime = i[6]
                #Print function to list time and date, not needed.
                #print("+ User: {}, last used: {}".format(i[0], lastTime))
                datetimelasttime = datetime.strptime(str(datetime.today()), self.zero.DATETIME_MASK)

                if not lastTime:
                    print("+ {} oldest so far.".format(i[0]))
                    oldestTime = datetimelasttime
                    currentSelect = count
                    break
                else:
                    datetimelasttime = datetime.strptime(lastTime, self.zero.DATETIME_MASK)

                if oldestTime >= datetimelasttime:
                    #oldestTime er nyere så setter forløpig denne til eldste
                    print("+ {} oldest so far.".format(i[0]))
                    oldestTime = datetimelasttime
                    currentSelect = count

                count += 1

            self.setCurrentUserUpdate(userList[currentSelect][0].strip(), userList[currentSelect][1].strip())

    def runUserCheck(self):
        print("\n- Loading INSTAGRAM user list from DB")
        userList = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_LOGIN_INSTA)
        if userList == 0:
            print("+ No user for Instagram found, please add one")
            user = input("+ Username: ")
            password = input("+ Password: ")
            email = input("+ Email: ")
            fullname = input("+ Fullname: ")

            print("+ Adding {} to DB".format(user))
            INSERT_DATA = (user, password, email, fullname, "instagram")
            self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_LOGIN_INSTA, INSERT_DATA)
            password = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_LOGIN_PASSWORD_INSTA , (user,))

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
                print("+ User list loaded.")
                return userList

    def editDefaultValue(self):
        getMaxValueFOLLOW = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, (self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT, ))[0][1]
        getMaxValueFOLLOWBY = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, (self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT, ))[0][1]
        getSurfaceScan = self.getValueSQL(conn, self.zero.DB_SELECT_OPTIONS, (self.zero.SURFACE_SCAN_TEXT, ))[0][1]

        print("\n- Loading default values:")
        print("+ Max allowed follow: {}".format(getMaxValueFOLLOW))
        print("+ Max allowed follow by: {}".format(getMaxValueFOLLOWBY))
        print("+ Surface scan set to: {} (0 = OFF, 1 = ON)".format(getMaxValueFOLLOWBY))

        change = input("+ Change value? [Y/n] ")

        if change.lower().strip() == "y":
            newMaxFollow = input("+ Max allowed follow: ")
            newMaxFollowBy = input("+ Max allowed followed by: ")
            newSurfaceScan = input("+ Surface scan on[1]/off[0]: ")

            if newMaxFollow.isdigit():
                if int(newMaxFollow) < 1:
                    print("+ Invalid input Max allowed follows not changed")
                else:
                    self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_OPTIONS, (newMaxFollow, self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT))
                    print("+ Max allowed follow set to: {}".format(newMaxFollow))
            else:
                print("+ Invalid input Max allowed follows not changed")

            if newMaxFollowBy.isdigit():
                if int(newMaxFollowBy) < 1:
                    print("+ Invalid input Max allowed followed by not changed")
                else:
                    self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_OPTIONS, (newMaxFollowBy, self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT))
                    print("+ Max allowed followed by set to: {}".format(newMaxFollowBy))
            else:
                print("+ Invalid input Max allowed followed by not changed")

            if newSurfaceScan.isdigit():
                if int(newMaxFollowBy) > 1:
                    print("+ Invalid input: Surface scan not changed")
                else:
                    if int(newMaxFollowBy) < 0:
                        print("+ Invalid input: Surface scan not changed")
                    else
                        self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_OPTIONS, (newSurfaceScan, self.zero.zero.SURFACE_SCAN_TEXT))
                        print("+ Surface scan set to: {}".format(newMaxFollowBy))
            else:
                print("+ Invalid input: Surface scan not changed")


        else:
            print("+ Nothing changed.")


    def addLastInsta(self, update):
        lastInsta = input("+ Enter account to scrape: ")
        print("+ Adding {} to DB".format(lastInsta))
        if update == False:
            self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_OPTIONS_LASTINSTA, ("last_insta", lastInsta))
        else:
            self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_LAST_INSTA, (lastInsta,))

        if lastInsta == 0:
            #Add loop for user
            print("+ Not able to add to scraper")
            sys.exit()

        else:
            self.zero.INSTA_USER = lastInsta
            print("+ Scraper enabled for: {}".format(self.zero.INSTA_USER))

    def lastSearch(self):
        print("\n- Loading last scraper for Instagram from DB")
        lastInsta = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, ("last_insta", ))
        if lastInsta == 0:
            print("+ No last search for Instagram found")
            self.addLastInsta(False)

        else:
            print("+ Last user scraped: {}".format(lastInsta[0][1]))
            goon = input("+ Continue with user? [Y/n] ")

            if goon.lower().strip() == "n":
                self.addLastInsta(True)
            else:
                self.zero.INSTA_USER = lastInsta[0][1]

    def setupLogin(self):
        userList = self.runUserCheck()
        if userList != True:
            print("+ User list imported")
            count = 0
            for i in userList:
                count += 1
                print("[{}] {} ({}) (Last used: {})".format(count, i[0], i[3].strip(), i[6]))
            selectUser = input("+ Select user (1-{}): ".format(count))

            if not selectUser.isnumeric():
                print("+ Invalid input, #1 selected")
                selectUser = 1

            if int(selectUser) > count:
                print("+ Invalid input, #1 selected")
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
        print("\n- Loading user and password from file")
        for file in self.zero.USER_FILES:
            fullpath = self.zero.OP_ROOT_FOLDER_PATH_VALUE + file[0]
            if os.path.isfile(fullpath):
                print("+ Found: {}, extracting data".format(fullpath))
                with open(fullpath) as fp:
                    line = fp.readline()
                    while line:
                        newUser = line.strip().split(",")

                        if len(newUser[0]) != 0:
                            #Check if exists
                            password = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_LOGIN_PASSWORD_INSTA , (newUser[0],))

                            if password != 0:
                                print("+ User allready exist: {}".format(newUser[0]))

                            else:
                                print("+ User NOT found adding user: {}. ".format(newUser[0]), end = " ")
                                INSERT_DATA = (newUser[0].strip(), newUser[1].strip(), newUser[2].strip(), newUser[3].strip(), newUser[4].strip())
                                self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_LOGIN_INSTA, INSERT_DATA)
                                password = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_LOGIN_PASSWORD_INSTA , (newUser[0].strip(),))

                                if password == 0:
                                    print("(Not able to add user)")
                                else:
                                    print("(User add OK)")
                        line = fp.readline()
            else:
                print("+ File: {} does not exist".format(fullpath))
