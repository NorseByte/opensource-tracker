import zerodata
from functions.instagram_func import *

class coreFunc():
    def __init__(self, dbTool, dbConn, instagram):
        self.dbTool = dbTool
        self.dbConn = dbConn
        self.instagram = instagram

    def find_between_r(s, first, last,):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""

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
        self.sourceID = self.dbTool.getValueSQL(self.dbConn, zerodata.DB_SELECT_ID_NODE, (self.currentUser.identifier, ))[0][0]
        print("+ Recived node ID:", self.sourceID, "for zeroPoint:", self.currentUser.username)

        #Setting global INSTA # IDEA
        zerodata.INSTA_USER_ID = self.currentUser.identifier

    def check_user_db_node(self, user, getInfo):
        print("+ Checking NODE DB for id: {} ({})".format(user.identifier, user.username,))
        if self.dbTool.getValueSQL(self.dbConn, zerodata.DB_SELECT_ID_NODE, (user.identifier, )) == 0:
            print("+ NOT found in node")
            tempID = user.identifier;

            if getInfo == True:
                print("+ Getting user data for: {}".format(user.username))
                user = self.instaTool.get_insta_account_info_id(tempID)

            print("+ Are full_name empty?", end = " ")
            if user.full_name:
                print("NO")
                print("+ Using: {} for label.".format(user.full_name))
                zerodata.INSERT_DATA = (user.full_name, user.full_name, user.identifier, user.get_profile_picture_url(), user.follows_count, user.followed_by_count, user.biography, user.username, user.is_private, user.is_verified, user.media_count, user.external_url)
            else:
                print("YES")
                print("+ Using: {} for label.".format(user.username))
                zerodata.INSERT_DATA = (user.full_name, user.username, user.identifier, user.get_profile_picture_url(), user.follows_count, user.followed_by_count, user.biography, user.username, user.is_private, user.is_verified, user.media_count, user.external_url)

            print("+ ADDING to NODE db")
            self.dbTool.inserttoTabel(self.dbConn, zerodata.DB_INSERT_NODE, zerodata.INSERT_DATA)
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
            getNewinsta = self.dbTool.getValueSQL(self.dbConn, zerodata.DB_SELECT_DONE_NEW_INSTA, (following.identifier, ))
            if getNewinsta == 0:
                insert_username = self.dbTool.getValueSQL(self.dbConn, zerodata.DB_SELECT_USERNAME_NODE, (following.identifier, ))[0][0]
                print("+ NOT found in new_insta adding user_id: {} ({})".format(following.identifier, insert_username))
                zerodata.INSERT_DATA = (following.identifier, insert_username)
                self.dbTool.inserttoTabel(self.dbConn, zerodata.DB_INSERT_NEW_INSTA, zerodata.INSERT_DATA)
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
            tempID = self.dbTool.getValueSQL(self.dbConn, zerodata.DB_SELECT_ID_NODE, (following.identifier, ))[0][0]
            print("+ Recived node ID: {} ({})".format(tempID, following.username))

            #Add in egdes_insta
            if inOut == True:
                print("+ Checking insta_edges DB. Source: {} ({}), Target: {} ({})".format(tempID, following.username, self.sourceID, self.currentUser.username))
                if self.dbTool.getValueSQL(self.dbConn, zerodata.DB_SELECT_TARGET_EDGE, (tempID, self.sourceID, )) == 0:
                    print("+ NOT found in insta_edges adding data.")
                    zerodata.INSERT_DATA = (tempID, self.sourceID)
                    self.dbTool.inserttoTabel(self.dbConn, zerodata.DB_INSERT_INSTA_EGDE, zerodata.INSERT_DATA)
                else:
                    print("+ FOUND in insta_edges list moving on")
            else:
                print("+ Checking insta_edges DB. Source: {} ({}), Target: {} ({})".format(self.sourceID, self.currentUser.full_name, tempID, following.username))
                if self.dbTool.getValueSQL(self.dbConn, zerodata.DB_SELECT_TARGET_EDGE, (self.sourceID, tempID, )) == 0:
                    print("+ NOT found in insta_edges adding data.")
                    zerodata.INSERT_DATA = (self.sourceID, tempID)
                    self.dbTool.inserttoTabel(self.dbConn, zerodata.DB_INSERT_INSTA_EGDE, zerodata.INSERT_DATA)
                else:
                    print("+ FOUND in insta_edges list moving on")
