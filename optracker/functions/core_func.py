from ..functions.instagram_func import *

class coreFunc():
    def __init__(self, dbTool, dbConn, instagram, Zero):
        self.dbTool = dbTool
        self.dbConn = dbConn
        self.instagram = instagram
        self.zero = Zero

    def find_between_r(s, first, last,):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def exportDBData(self):
        print("\n- Loading current data from DB")
        totalNodes = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_COUNT_NODES)[0][0]
        totalEdgesInsta = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_COUNT_EDES_INSTA)[0][0]
        print("+ Total nodes: {}\n+ Total egdes from instagram:{}".format(totalNodes, totalEdgesInsta))
        exportyes = input("+ Do you want to export? (D:Y Y/N) ")

        if exportyes.lower().strip() != "n":
            print("+ Exporting NODES")
            self.dbTool.exportNode(self.dbConn, self.zero.DB_SELECT_ALL_NODE, self.zero.DB_DATABASE_EXPORT_NODES)
            print("+ NODES exported to: {}".format(self.zero.DB_DATABASE_EXPORT_NODES))

            print("+ Exporting EDGES")
            self.dbTool.exportNode(self.dbConn, self.zero.DB_SELECT_ALL_INSTA_EDGES, self.zero.DB_DATABASE_EXPORT_INSTA_EGDE)
            print("+ EDGES exported to: {}".format(self.zero.DB_DATABASE_EXPORT_INSTA_EGDE))

    def getDoneUserIDFromInsta(self):
        print("\n- Loading done user from instagram")
        userList = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_ALL_DONE_NEW_INSTA)

        if userList == 0:
            print("+ No users in database that have been scannet 100%")
            return 0

        else:
            print("+ User list imported")
            count = 0
            for i in userList:
                count += 1
                print("[{}] {} ({})".format(count, i[0], i[1].strip()))
            selectUser = input("+ Select user (1-{}): ".format(count))

            if not selectUser.isnumeric():
                print("+ Invalid input, #1 selected")
                selectUser = 1

            if int(selectUser) > count:
                print("+ Invalid input, #1 selected")
                selectUser = 1

            newNumber = int(selectUser) - 1
            return userList[newNumber]

    def scanFollowToInstaID(self):
        currentInstaID = self.getDoneUserIDFromInsta()

        print("\n- Starting scan by follow")
        if currentInstaID == 0:
            print("+ No users could be selected.\n+ Run a full scan of a user to continue.")

        else:
            currentUser = currentInstaID[1]
            currentID = currentInstaID[0]

            getMaxValueFOLLOW = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, (self.zero.INSTA_MAX_FOLLOW_SCAN_TEXT, ))[0][1]
            getMaxValueFOLLOWBY = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_OPTIONS, (self.zero.INSTA_MAX_FOLLOW_BY_SCAN_TEXT, ))[0][1]

            print("+ Current insta id: {} ({})".format(currentID, currentUser))
            print("+ Looking up NODE ID.")
            currentNode = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ID_NODE, (currentID, ))[0][0]
            print("+ Node ID found: {}".format(currentNode))
            print("+ Loading followed by list where PRIVATE = 0")
            followList = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_FOLLOW_OF, (currentNode, ))
            if followList == 0:
                print("+ Are followed nobody that have PUBLIC profile.")
            else:
                lenFollowList = len(followList)
                counter = 0
                print("+ Loaded {} users from: {} where private = 0".format(lenFollowList, currentUser))

                #TODO: ADD SORTING OF USER BASED ON KEY WORD FROM BIO
                for i in followList:
                    counter += 1
                    print("\n- {} of {} :: {}".format(counter, lenFollowList, i[8])),
                    print("+ Checking search status for: {}".format(i[3]))
                    moveON = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_DONE_NEW_INSTA, (i[3],))
                    if moveON[0][0] == 1:
                        print("+ User SCAN are allready DONE.")
                    else:
                        if moveON[0][1] == 1:
                            print("+ User NOT scanned but set on WAIT")
                        else:
                            #Search sorting firt step follows_count
                            print("+ User VALID for singel scan.")

                            scan_insta_followed_by = int(i[6])
                            scan_insta_follow = int(i[5])

                            print("+ User are following: {}\n+ User are followed by: {}".format(scan_insta_follow, scan_insta_followed_by))

                            if scan_insta_follow <= getMaxValueFOLLOW:
                                if scan_insta_followed_by <= getMaxValueFOLLOWBY:
                                    #Search critera for allowed OK Start scan.
                                    self.setCurrentUser(i[8].strip())

                                    #Extract info from following list
                                    self.loadFollowlist(False)
                                    self.add_egde_from_list_insta(False)

                                    #Extract followed by
                                    self.loadFollowlist(True)
                                    self.add_egde_from_list_insta(True)

                                    #Update new_Insta
                                    print("\n- Scan complete")
                                    print("+ Setting {} ({}) to complete.".format(i[8], i[3]))
                                    self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_NEW_INSTA_DONE_TRUE, (i[3],))
                                else:
                                    print("+ User are followed by to many, increese allowed follow to continue")
                            else:
                                print("+ User are following to many, increese allowed follow to continue")


    def loadFollowlist(self, inOut): #False load Follow, True Load followers
        if inOut == False:
            #Getting following
            print("\n- Loading follows list for:", self.currentUser.username)
            self.followNumber = self.currentUser.follows_count;
            print("+", self.currentUser.full_name, "are following", self.followNumber, "starting info extract")
            self.imported_follow = self.instaTool.get_insta_following(self.followNumber, self.currentUser.identifier)
            self.lenImpF = len(self.imported_follow['accounts'])
            print("+ Total loaded:", self.lenImpF)
        else:
            #Getting following
            print("\n- Loading followed by list for:", self.currentUser.username)
            self.followNumber = self.currentUser.followed_by_count;
            print("+", self.currentUser.full_name, "are followed by", self.followNumber, "starting info extract")
            self.imported_follow = self.instaTool.get_insta_follow_by(self.followNumber, self.currentUser.identifier)
            self.lenImpF = len(self.imported_follow['accounts'])
            print("+ Total loaded:", self.lenImpF)

    def setCurrentUser(self, user):
        #Get information
        print("\n- Setting current user to:", user)
        self.instaTool = InstagramFunc(self.instagram, user)

        #Check if zeroPoint is in DB if not add.
        print("+ Getting user information from Instagram")
        self.currentUser = self.instaTool.get_insta_account_info(user)
        self.check_user_db_node(self.currentUser, False)

        #Getting current NODE ID for source
        self.sourceID = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ID_NODE, (self.currentUser.identifier, ))[0][0]
        print("+ Recived node ID:", self.sourceID, "for zeroPoint:", self.currentUser.username)

        #Setting global INSTA # IDEA
        self.zero.INSTA_USER_ID = self.currentUser.identifier

    def check_user_db_node(self, user, getInfo):
        print("+ Checking NODE DB for id: {} ({})".format(user.identifier, user.username,))
        if self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ID_NODE, (user.identifier, )) == 0:
            print("+ NOT found in node")
            tempID = user.identifier;

            if getInfo == True:
                print("+ Getting user data for: {}".format(user.username))
                user = self.instaTool.get_insta_account_info_id(tempID)

            print("+ Are full_name empty?", end = " ")
            if user.full_name:
                print("NO")
                print("+ Using: {} for label.".format(user.full_name))
                self.zero.INSERT_DATA = (user.full_name, user.full_name, user.identifier, user.get_profile_picture_url(), user.follows_count, user.followed_by_count, user.biography, user.username, user.is_private, user.is_verified, user.media_count, user.external_url)
            else:
                print("YES")
                print("+ Using: {} for label.".format(user.username))
                self.zero.INSERT_DATA = (user.full_name, user.username, user.identifier, user.get_profile_picture_url(), user.follows_count, user.followed_by_count, user.biography, user.username, user.is_private, user.is_verified, user.media_count, user.external_url)

            print("+ ADDING to NODE db")
            self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_NODE, self.zero.INSERT_DATA)
        else:
            print("+ FOUND in NODE list moving on")

    def add_egde_from_list_insta(self, inOut):
        counterF = 0
        for following in self.imported_follow['accounts']:
            counterF += 1
            print("\n- {} of {} :: Username: {} - ID: {}".format(counterF, self.lenImpF, following.username, following.identifier))

            #Add in Node DB
            self.check_user_db_node(following, True)

            #Check if this is a new node that havent been search
            print("+ Checking new_insta DB for: {}".format(following.identifier))
            getNewinsta = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_DONE_NEW_INSTA, (following.identifier, ))
            if getNewinsta == 0:
                insert_username = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_USERNAME_NODE, (following.identifier, ))[0][0]
                print("+ NOT found in new_insta adding user_id: {} ({})".format(following.identifier, insert_username))
                self.zero.INSERT_DATA = (following.identifier, insert_username)
                self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_NEW_INSTA, self.zero.INSERT_DATA)
            else:
                print("+ FOUND in new_insta STATUS = ", end = " ")
                if getNewinsta[0][0] == 1:
                    print("FINNISH")
                else:
                    if getNewinsta[0][1] == 1:
                        print("WAIT")
                    else:
                        print("IN LINE")

            #Get node ID
            tempID = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ID_NODE, (following.identifier, ))[0][0]
            print("+ Recived node ID: {} ({})".format(tempID, following.username))

            #Add in egdes_insta
            if inOut == True:
                print("+ Checking insta_edges DB. Source: {} ({}), Target: {} ({})".format(tempID, following.username, self.sourceID, self.currentUser.username))
                if self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_TARGET_EDGE, (tempID, self.sourceID, )) == 0:
                    print("+ NOT found in insta_edges adding data.")
                    self.zero.INSERT_DATA = (tempID, self.sourceID)
                    self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_INSTA_EGDE, self.zero.INSERT_DATA)
                else:
                    print("+ FOUND in insta_edges list moving on")
            else:
                print("+ Checking insta_edges DB. Source: {} ({}), Target: {} ({})".format(self.sourceID, self.currentUser.full_name, tempID, following.username))
                if self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_TARGET_EDGE, (self.sourceID, tempID, )) == 0:
                    print("+ NOT found in insta_edges adding data.")
                    self.zero.INSERT_DATA = (self.sourceID, tempID)
                    self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_INSTA_EGDE, self.zero.INSERT_DATA)
                else:
                    print("+ FOUND in insta_edges list moving on")
