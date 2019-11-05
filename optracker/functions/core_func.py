import os
import requests
import shutil
import filecmp
import imghdr
from PIL import Image
from ..functions.instagram_func import *

class coreFunc():
    def __init__(self, dbTool, dbConn, instagram, Zero, Facerec):
        self.dbTool = dbTool
        self.dbConn = dbConn
        self.instagram = instagram
        self.zero = Zero
        self.instaTool = InstagramFunc(self.instagram)
        self.curPrivate = 0
        self.facerec = Facerec

    def find_between_r(self, s, first, last,):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def is_similar(self, image1, image2):
        return filecmp.cmp(image1, image2)

    def createFolderIf(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
            self.zero.printText("+ Folder created: {}".format(folder), False)
        else:
            self.zero.printText("+ Folder loacted: {}".format(folder), False)

    def setImageName(self, folder, username, type):
        c = 1
        d = True
        currentFile = ""
        while d == True:
            currentFile = folder + username + "-" + str(c) + type
            if os.path.isfile(currentFile) == False:
                d = False
            else:
                self.zero.printText("+ File: {} exist trying next.".format(currentFile), False)
                c += 1

        self.zero.printText("+ Setting filename: {}".format(currentFile), False)
        return currentFile

    def compareImage(self, path, currentFile):
        #Get files in directory # r=root, d=directories, f = files
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                    files.append(os.path.join(r, file))

        #Check if its the only ones
        for f in files:
            if f != currentFile:
                self.zero.printText("+ Checking {} and {} if same.".format(currentFile, f), False)
                if self.is_similar(currentFile, f) == True:
                    self.zero.printText("+ Image same deleting: {}".format(currentFile), False)
                    os.remove(currentFile)
                    return True
        return False

    def createInstaProfileFolder(self, ID):
        curr = self.zero.OP_INSTA_PROFILEFOLDER_NAME_VALUE
        counter = 1

        for i in range(0, len(ID), 2):
            if counter <= 2:
                curr = curr + ID[i:i + 2] + '\\'
                self.createFolderIf(curr)
                counter += 1

        curr = curr + ID + "\\"
        self.createFolderIf(curr)
        return curr

    def downloadProfileImage(self, name, username, type, url):
        instaFolder = self.createInstaProfileFolder(name)
        file = self.setImageName(instaFolder, username, type)

        self.zero.printText("+ Downloading Image: {}".format(file), True)
        downloadok = True

        #Write Image
        resp = requests.get(url, stream=True)
        local_file = open(file, 'wb')
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, local_file)
        local_file.close()
        del resp

        #Read Image to verify
        type = imghdr.what(file)

        if str(type) != "None":
            self.zero.printText("+ Download Complete", True)
        else:
            downloadok = False
            self.zero.printText("+ File dont contain image, deleting file", True)
            os.remove(file)

        if downloadok == True:
            if self.compareImage(instaFolder, file) == False:
                if int(self.zero.FACEREC_ON_VALUE) == int(1):
                    self.zero.printText("+ Face scan active, scanning image", True)
                    face, image = self.facerec.findFaceinImg(file)
                    if len(face) == 0:
                        self.zero.printText("+ Found no face in image, deleting file", True)
                        os.remove(file)
                    else:
                        self.zero.printText("+ Found {} faces in image".format(len(face)), True)

    def exportDBData(self):
        self.zero.printText("\n- Loading current data from DB", True)
        totalNodes = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_COUNT_NODES)[0][0]
        totalEdgesInsta = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_COUNT_EDES_INSTA)[0][0]
        self.zero.printText("+ Total nodes: {}\n+ Total egdes from instagram:{}".format(totalNodes, totalEdgesInsta), True)
        exportyes = input("+ Do you want to export? [Y/n] ")

        if exportyes.lower().strip() != "n":
            self.zero.printText("+ Exporting NODES", True)
            self.dbTool.exportNode(self.dbConn, self.zero.DB_SELECT_EXPORT_ID_USER, self.zero.DB_DATABASE_EXPORT_FOLDER + self.zero.DB_DATABASE_EXPORT_NODES)
            self.zero.printText("+ NODES exported to: {}".format(self.zero.DB_DATABASE_EXPORT_NODES), True)

            self.zero.printText("+ Exporting EDGES", True)
            self.dbTool.exportNode(self.dbConn, self.zero.DB_SELECT_ALL_INSTA_EDGES, self.zero.DB_DATABASE_EXPORT_FOLDER + self.zero.DB_DATABASE_EXPORT_INSTA_EGDE)
            self.zero.printText("+ EDGES exported to: {}".format(self.zero.DB_DATABASE_EXPORT_INSTA_EGDE), True)

    def getDoneUserIDFromInsta(self):
        self.zero.printText("\n- Loading done user from instagram", True)
        userList = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_ALL_DONE_NEW_INSTA)

        if userList == 0:
            self.zero.printText("+ No users in database that have been scannet 100%", True)
            return 0

        else:
            self.zero.printText("+ User list imported", True)
            count = 0
            for i in userList:
                count += 1
                self.zero.printText("[{}] {} ({})".format(count, i[0], str(i[1]).strip()), True)
            selectUser = input("+ Select user (1-{}): ".format(count))

            if not selectUser.isnumeric():
                self.zero.printText("+ Invalid input, #1 selected", True)
                selectUser = 1

            if int(selectUser) > count:
                self.zero.printText("+ Invalid input, #1 selected", True)
                selectUser = 1

            newNumber = int(selectUser) - 1
            return userList[newNumber]

    def updateNodesUser(self, instaID):
        self.zero.printText("+ Updating user data for: {}".format(instaID), False)
        newDataUser = self.instaTool.get_insta_account_info_id(instaID)
        self.zero.printText("+ User data loaded.", False)
        label = self.getLabelforUser(newDataUser)

        #Download profile Image
        if int(self.zero.DOWNLOAD_PROFILE_INSTA_VALUE) == 1:
            self.downloadProfileImage(newDataUser.identifier, newDataUser.username, self.zero.INSTA_FILE_EXT, newDataUser.get_profile_picture_url())

        UPDATE_DATA = (self.zero.sanTuple(newDataUser.full_name), self.zero.sanTuple(label), newDataUser.get_profile_picture_url(), newDataUser.follows_count, newDataUser.followed_by_count, self.zero.sanTuple(newDataUser.biography), newDataUser.username, newDataUser.is_private, newDataUser.is_verified, newDataUser.media_count, newDataUser.external_url, 1,  newDataUser.identifier)
        self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_NODES, UPDATE_DATA)
        self.zero.printText("+ Update of DB NODE complete.", False)
        return newDataUser

    def updateProfileImg(self):
        self.zero.printText("\n- Starting Profile Img Update", True)
        user_img_list = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_IMG)
        lengList = len(user_img_list)
        counter = 1
        for u in user_img_list:
            self.zero.printText("\n+ {} of {}: {}".format(counter, lengList, u[0]), True)
            counter += 1
            #Download profile Image
            self.downloadProfileImage(str(u[1]), str(u[0]), self.zero.INSTA_FILE_EXT, str(u[2]))

    def updateNodesUserLoaded(self, newDataUser):
        self.zero.printText("+ Updating user data for: {} ({})".format(newDataUser.username, newDataUser.identifier), False)
        label = self.getLabelforUser(newDataUser)
        UPDATE_DATA = (self.zero.sanTuple(newDataUser.full_name), self.zero.sanTuple(label), newDataUser.get_profile_picture_url(), newDataUser.follows_count, newDataUser.followed_by_count, self.zero.sanTuple(newDataUser.biography), newDataUser.username, newDataUser.is_private, newDataUser.is_verified, newDataUser.media_count, newDataUser.external_url, 1,  newDataUser.identifier)
        self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_NODES, UPDATE_DATA)
        self.zero.printText("+ Update of DB NODE complete.", False)

    def updateNodeFromList(self):
        self.zero.printText("\n- Updating users from list", True)
        fullpath = self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.USER_FILE_SCAN_NODE_INSTA
        if os.path.isfile(fullpath):
            self.zero.printText("+ Found: {}, extracting data".format(fullpath), True)
            with open(fullpath) as fp:
                line = fp.readline()
                while line:
                    if line != 0:
                        user = line.strip()
                        zero.printText("+ Getting user info for {}:".format(user), True)
                        updatenode = self.instaTool.get_insta_account_info(user)

                        #Download profile Image
                        if int(self.zero.DOWNLOAD_PROFILE_INSTA_VALUE) == 1:
                            self.downloadProfileImage(updatenode.identifier, updatenode.username, self.zero.INSTA_FILE_EXT, updatenode.get_profile_picture_url())

                        self.updateNodesUserLoaded(updatenode)
                    line = fp.readline()
        else:
            self.zero.printText("+ File not found.", True)
            self.zero.printText("+ Create {} to continue.".format(fullpath), True)

    def deepScanAll(self):
        self.zero.printText("\n-Geting users from DB", True)
        allDeep = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_DEEPSCAN_NEED)
        lengDeep = len(allDeep)
        counter = 1
        for u in allDeep:
            user = u[0]
            self.zero.printText("+ {} of {} - Getting user info for {}:".format(counter, lengDeep, user), True)
            updatenode = self.instaTool.get_insta_account_info(user)

            #Download profile Image
            if int(self.zero.DOWNLOAD_PROFILE_INSTA_VALUE) == 1:
                self.downloadProfileImage(updatenode.identifier, updatenode.username, self.zero.INSTA_FILE_EXT, updatenode.get_profile_picture_url())

            self.updateNodesUserLoaded(updatenode)
            counter += 1

    def scanFollowToInstaID(self):
        currentInstaID = self.getDoneUserIDFromInsta()

        self.zero.printText("\n- Starting scan by follow", True)
        if currentInstaID == 0:
            self.zero.printText("+ No users could be selected.\n+ Run a full single scan of a user to continue.", True)

        else:
            currentUser = currentInstaID[1]
            currentID = currentInstaID[0]

            getMaxValueFOLLOW = int(self.zero.INSTA_MAX_FOLLOW_SCAN_VALUE)
            getMaxValueFOLLOWBY = int(self.zero.INSTA_MAX_FOLLOW_BY_SCAN_VALUE)

            self.zero.printText("+ Current insta id: {} ({})".format(currentID, currentUser), True)
            self.zero.printText("+ Looking up NODE ID.", True)
            currentNode = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ID_NODE, (currentID, ))[0][0]
            self.zero.printText("+ Node ID found: {}".format(currentNode), True)
            self.zero.printText("+ Loading followed by list where PRIVATE = 0", True)
            followList = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_FOLLOW_OF, (currentNode, ))
            if followList == 0:
                self.zero.printText("+ Are followed nobody that have PUBLIC profile.", True)
            else:
                lenFollowList = len(followList)
                counter = 0
                self.zero.printText("+ Loaded {} users from: {} where private = 0".format(lenFollowList, currentUser), True)

                #TODO: ADD SORTING OF USER BASED ON KEY WORD FROM BIO
                for i in followList:
                    counter += 1
                    self.zero.printText("\n- {} of {} :: {}".format(counter, lenFollowList, i[8]), True),
                    self.zero.printText("+ Checking search status for: {}".format(i[3]), False)
                    moveON = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_DONE_NEW_INSTA, (i[3],))
                    if moveON[0][0] == 1:
                        self.zero.printText("+ User SCAN are allready DONE.", True)
                    else:
                        if moveON[0][1] == 1:
                            self.zero.printText("+ User NOT scanned but set on WAIT", True)
                        else:
                            self.zero.printText("+ User VALID for singel scan.", True)

                            scan_insta_followed_by = int(i[6])
                            scan_insta_follow = int(i[5])

                            #TODO: SPEEDUP SCAN - LESS SQL REQUEST
                            deepScan = int(i[13])
                            if deepScan == 0:
                                #User have not been deepscanned scan and update
                                self.zero.printText("+ User missing deepScan, getting info.", False)
                                newDataUser = self.updateNodesUser(i[3])
                                scan_insta_followed_by = int(newDataUser.followed_by_count)
                                scan_insta_follow = int(newDataUser.follows_count)


                            self.zero.printText("+ User are following: {}\n+ User are followed by: {}".format(scan_insta_follow, scan_insta_followed_by), False)

                            #Search sorting firt step follows_count
                            if scan_insta_follow <= getMaxValueFOLLOW:
                                if scan_insta_followed_by <= getMaxValueFOLLOWBY:
                                    #Search critera for allowed OK Start scan.
                                    self.setCurrentUser(i[8].strip())

                                    #Check if private
                                    if self.curPrivate == 0:
                                        #Extract info from following list
                                        if scan_insta_follow != 0:
                                            if self.loadFollowlist(False) == True:
                                                self.add_egde_from_list_insta(False)
                                        else:
                                            self.zero.printText("+ Follow list is empty", False)

                                        #Extract followed by
                                        if scan_insta_followed_by != 0:
                                            if self.loadFollowlist(True) == True:
                                                self.add_egde_from_list_insta(True)
                                        else:
                                            self.zero.printText("+ Follow by list is empty", False)

                                        #Update new_Insta
                                        self.zero.printText("\n- Scan complete", False)
                                        self.zero.printText("+ Setting {} ({}) to complete.".format(i[8], i[3]), True)
                                        self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_NEW_INSTA_DONE_TRUE, (i[3],))
                                    else:
                                        self.zero.printText("+ User profile are private after update.", True)
                                        self.zero.printText("+ Setting {} ({}) to complete.".format(i[8], i[3]), True)
                                        self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_NEW_INSTA_DONE_TRUE, (i[3],))
                                else:
                                    self.zero.printText("+ User are followed by to many, increese allowed follow to continue", True)
                            else:
                                self.zero.printText("+ User are following to many, increese allowed follow to continue", True)


    def loadFollowlist(self, inOut): #False load Follow, True Load followers
        continueScan = True

        if inOut == False:
            #Getting following
            self.zero.printText("\n- Loading follows list for: {}".format(self.currentUser.username), True)
            self.followNumber = self.currentUser.follows_count;
            if self.followNumber != 0:
                self.zero.printText("+ {} are following {} starting info extract.".format(self.currentUser.full_name, self.followNumber), False)
                self.imported_follow = self.instaTool.get_insta_following(self.followNumber, self.currentUser.identifier)
                self.lenImpF = len(self.imported_follow['accounts'])
                self.zero.printText("+ Total loaded: {}".format(self.lenImpF), False)
                continueScan = True
            else:
                print("+ {} are following NOBODY, skipping this stage".format(self.currentUser.username))
                continueScan = False
        else:
            #Getting following
            self.zero.printText("\n- Loading followed by list for: {}".format(self.currentUser.username), True)
            self.followNumber = self.currentUser.followed_by_count;
            if self.followNumber != 0:
                self.zero.printText("+ {} are followed by {} starting info extract".format(self.currentUser.full_name, self.followNumber), False)
                self.imported_follow = self.instaTool.get_insta_follow_by(self.followNumber, self.currentUser.identifier)
                self.lenImpF = len(self.imported_follow['accounts'])
                self.zero.printText("+ Total loaded: {}".format(self.lenImpF), False)
                continueScan = True
            else:
                print("+ {} are following NOBODY, skipping this stage".format(self.currentUser.username))
                continueScan = False

        return continueScan

    def setCurrentUser(self, user):
        #Get information
        self.zero.printText("\n- Setting current user to: {}".format(user), True)

        #Check if zeroPoint is in DB if not add.
        self.zero.printText("+ Getting user information from Instagram", True)
        self.currentUser = self.instaTool.get_insta_account_info(user)
        self.curPrivate = self.currentUser.is_private
        self.check_user_db_node(self.currentUser, False)

        #Download profile Image
        if int(self.zero.DOWNLOAD_PROFILE_INSTA_VALUE) == 1:
            self.downloadProfileImage(self.currentUser.identifier, self.currentUser.username, self.zero.INSTA_FILE_EXT, self.currentUser.get_profile_picture_url())

        #Update User information
        self.updateNodesUserLoaded(self.currentUser)

        #Check if in new_Insta
        self.check_new_insta(self.currentUser.identifier, self.currentUser.username)

        #Getting current NODE ID for source
        self.sourceID = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ID_NODE, (self.currentUser.identifier, ))[0][0]
        self.zero.printText("+ Recived node ID: {} for zeroPoint: {}".format(self.sourceID, self.currentUser.username), True)

        #Setting global INSTA # IDEA
        self.zero.printText("+ Global insta ID set to {}".format(self.currentUser.identifier), True)
        self.zero.INSTA_USER_ID = self.currentUser.identifier

    def check_new_insta(self, instaID, insert_username):
        self.zero.printText("+ Checking new_insta DB for: {}".format(instaID), False)
        getNewinsta = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_DONE_NEW_INSTA, (instaID, ))
        if getNewinsta == 0:
            self.zero.printText("+ NOT found in new_insta adding user_id: {} ({})".format(instaID, insert_username), False)
            self.zero.INSERT_DATA = (instaID, insert_username)
            self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_NEW_INSTA, self.zero.INSERT_DATA)
        else:
            self.zero.printText("+ FOUND in new_insta", False)
            if getNewinsta[0][0] == 1:
                self.zero.printText("+ STATUS = FINNISH", False)
            else:
                if getNewinsta[0][1] == 1:
                    self.zero.printText("+ STATUS = WAIT", False)
                else:
                    self.zero.printText("+ STATUS = IN LINE", False)

    def getLabelforUser(self, user):
        self.zero.printText("+ Are full_name empty?", False)
        if user.full_name:
            self.zero.printText("+ NO", False)
            self.zero.printText("+ Using: {} for label.".format(user.full_name), False)
            return user.full_name

        else:
            self.zero.printText("+ YES", False)
            self.zero.printText("+ Using: {} for label.".format(user.username), False)
            return user.username

    def check_user_db_node(self, user, getInfo):
        #Check if we do a full scan
        getSurfaceScan = int(self.zero.SURFACE_SCAN_VALUE)

        #Get node id
        userNodeID = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ID_NODE, (user.identifier, ))

        self.zero.printText("+ Checking NODE DB for id: {} ({})".format(user.identifier, user.username), False)
        if userNodeID == 0:
            self.zero.printText("+ NOT found in node", False)
            tempID = user.identifier;

            if getSurfaceScan == 0:
                if getInfo == True:
                    self.zero.printText("+ Getting user data for: {}".format(user.username), False)
                    user = self.instaTool.get_insta_account_info_id(tempID)

                    #Download profile
                    if int(self.zero.DOWNLOAD_PROFILE_INSTA_VALUE) == 1:
                        self.downloadProfileImage(user.identifier, user.username, self.zero.INSTA_FILE_EXT, user.get_profile_picture_url())

                label = self.getLabelforUser(user)
                self.zero.INSERT_DATA = (self.zero.sanTuple(user.full_name), self.zero.sanTuple(label), user.identifier, user.get_profile_picture_url(), user.follows_count, user.followed_by_count, self.zero.sanTuple(user.biography), user.username, user.is_private, user.is_verified, user.media_count, user.external_url, 1, user.identifier)

            else:
                #TODO: Add image download to surface`?
                self.zero.printText("+ Surfacescan are ON", False)

                if user.is_private == False:
                    user.is_private = 0
                else:
                    user.is_private = 1

                if user.is_verified == False:
                    user.is_verified = 0
                else:
                    user.is_verified = 1

                label = self.getLabelforUser(user)
                self.zero.INSERT_DATA = (self.zero.sanTuple(user.full_name), self.zero.sanTuple(label), user.identifier, user.get_profile_picture_url(), user.follows_count, user.followed_by_count, self.zero.sanTuple(user.biography), user.username, user.is_private, user.is_verified, user.media_count, user.external_url, 0, user.identifier)

            self.zero.printText("+ ADDING to NODE db", False)
            userNodeID = self.dbTool.inserttoTabelMulti(self.dbConn, self.zero.DB_INSERT_NODE, self.zero.INSERT_DATA)[0][0]
        else:
            userNodeID = userNodeID[0][0]
            self.zero.printText("+ FOUND in NODE list ({}) moving on".format(userNodeID), False)

        return userNodeID

    def add_egde_from_list_insta(self, inOut):
        counterF = 0
        for following in self.imported_follow['accounts']:
            counterF += 1
            self.zero.printText("\n", False)
            self.zero.printText("- {} of {} :: Username: {} - ID: {}".format(counterF, self.lenImpF, following.username, following.identifier), True)

            #Add in Node DB
            tempID = self.check_user_db_node(following, True)

            #Check if this is a new node that havent been search
            self.check_new_insta(following.identifier, following.username)

            #Get node ID
            self.zero.printText("+ Recived node ID: {} ({})".format(tempID, following.username), False)

            #Add in egdes_insta
            if inOut == True:
                self.zero.printText("+ Checking insta_edges DB. Source: {} ({}), Target: {} ({})".format(tempID, following.username, self.sourceID, self.currentUser.username), False)
                if self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_TARGET_EDGE, (tempID, self.sourceID, )) == 0:
                    self.zero.printText("+ NOT found in insta_edges adding data", False)
                    self.zero.INSERT_DATA = (tempID, self.sourceID)
                    self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_INSTA_EGDE, self.zero.INSERT_DATA)
                else:
                    self.zero.printText("+ FOUND in insta_edges list moving on", False)
            else:
                self.zero.printText("+ Checking insta_edges DB. Source: {} ({}), Target: {} ({})".format(self.sourceID, self.currentUser.full_name, tempID, following.username), False)
                if self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_TARGET_EDGE, (self.sourceID, tempID, )) == 0:
                    self.zero.printText("+ NOT found in insta_edges adding data.", False)
                    self.zero.INSERT_DATA = (self.sourceID, tempID)
                    self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_INSERT_INSTA_EGDE, self.zero.INSERT_DATA)
                else:
                    self.zero.printText("+ FOUND in insta_edges list moving on", False)
