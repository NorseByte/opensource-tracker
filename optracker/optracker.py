import os
from sys import argv
from .zerodata import zerodata
from .functions.db_func import dbFunc
from .functions.side_func import sideFunc
from .functions.core_func import coreFunc
from .igramscraper.instagram import Instagram
from .facerec.facerec import facerec
from .functions.statinfo import statInfo
from time import sleep
from tabulate import tabulate

class Optracker():
    def __init__(self, offline):
        #Adding Text source
        self.zero = zerodata()

        #Sett ofline to false or true
        self.zero.RUN_OFFLINE = offline

        #Setting up OP_ROOT_FOLDER
        self.createRootfolder()

        #Load Config
        self.zero.setupJSON(False)

        #Load face_recognition
        self.myFace = facerec(self.zero)

        #Iniatlaize DB_DATABASE
        print("+ Setting up DB")
        self.dbTool = dbFunc(self.zero.DB_DATABASE, self.zero)
        self.dbConn =  self.dbTool.create_connection()

        #Create Tabels
        if self.zero.DB_MYSQL_ON == 0:
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_NODES)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_EGDES)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_NEW_INSTA)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_LOGIN_INSTA)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_OPTIONS)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MEDIA)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MEDIA_LINKS)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MEDIA_COMMENT)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MEDIA_LIKE)
        else:
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_NODES)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_EGDES)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_NEW_INSTA)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_LOGIN_INSTA)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_OPTIONS)

        self.dbTool.setDefaultValueOptions(self.dbConn)
        self.zero.printText("+ DB setup complete", False)
        
        #Setup side tools
        self.sideTool = sideFunc(self.dbTool, self.dbConn, self.zero)
        
        #Get username
        self.sideTool.loadLoginText()
        self.sideTool.countCurrentUser()

        #Init INSTAGRAM
        self.instagram = Instagram()

        if self.zero.RUN_OFFLINE == False:
            #User Select and Login
            self.autoSelectAndLogin()

        #Setup coreFunc
        print("+ Setting up core functions")
        self.mainFunc = coreFunc(self.dbTool, self.dbConn, self.instagram, self.zero, self.myFace)

        #Setup Stat dbTool, dbConn, Zero
        self.userStat = statInfo(self.dbTool, self.dbConn, self.zero)

        self.MENU_ITEMS_ONLINE = [
            { self.zero.HELP_TEXT_DISP: self.dispHelp },
            { self.zero.RUN_CURRENT_DISP: self.runSingelScan },
            { self.zero.RUN_FOLLOW_DISP: self.runFollowScan },
            { self.zero.RUN_CHANGE_USER: self.selectUserAndLogin },
            { self.zero.RUN_LOAD_SCAN: self.runLoadUserNodeScan },
            { self.zero.RUN_EXPORT_DATA: self.dispExport},
            { self.zero.RUN_EDIT_OPTIONS: self.runEditDefault},
            { self.zero.RUN_GET_DEEP: self.runDeepfromDB},
            { self.zero.RUN_UPDATE_IMG: self.updateImg},
            { self.zero.RUN_DOWNLOAD_POST: self.updatePost},
            { self.zero.RUN_VIEW_STAT: self.runStat},
            { self.zero.RUN_EXIT_DISP: exit},
        ]

        self.MENU_ITEMS_OFFLINE = [
            { self.zero.HELP_TEXT_DISP: self.dispHelp },
            { self.zero.RUN_EXPORT_DATA: self.dispExport},
            { self.zero.RUN_EDIT_OPTIONS: self.runEditDefault},
            { self.zero.RUN_VIEW_STAT: self.runStat},
            { self.zero.RUN_EXIT_DISP: exit},
        ]

        if self.zero.RUN_OFFLINE == False: self.MENU_ITEMS = self.MENU_ITEMS_ONLINE
        else: self.MENU_ITEMS = self.MENU_ITEMS_OFFLINE

    #Run stat
    def runStat(self):
        self.userStat.getStatforUserNode()
        input("+ Press [Enter] to continue...")

    #Core Functions to main
    def runSingelScan(self):
        #Setup zeroPoint
        self.sideTool.lastSearch()

        #Run Scan from zeroPoint
        self.mainFunc.setCurrentUser(self.zero.INSTA_USER)
        self.runCurrentScan()

    def updateImg(self):
        self.mainFunc.updateProfileImg()

    def updatePost(self):
        #Setup zeroPoint
        self.sideTool.lastSearch()

        #Downloading user post
        self.mainFunc.setCurrentUser(self.zero.INSTA_USER)

        if int(self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_DEEPPOST, (self.mainFunc.currentUser.identifier, ))[0][0]) == 1:
            if input("+ User are allready scanned, continue? [y/N] ").lower().strip() == "y":self.mainFunc.downloadCurrentUserPost()
        else:self.mainFunc.downloadCurrentUserPost()

    def selectUserAndLogin(self):
        #Setusername
        self.sideTool.setupLogin()
        #Login Instagram
        self.loginInstagram(self.instagram)

    def autoSelectAndLogin(self):
        #Find user
        self.sideTool.autoSelectLogin()
        #Login instagram
        self.loginInstagram(self.instagram)

    def runCurrentScan(self):
        #Extract info from following list
        if self.mainFunc.loadFollowlist(False) == True:
            self.mainFunc.add_egde_from_list_insta(False)

        #Extract followed by
        if self.mainFunc.loadFollowlist(True) == True:
            self.mainFunc.add_egde_from_list_insta(True)

        #Update new_Insta
        print("\n- Scan complete")
        print("+ Setting {} ({}) to complete.".format(self.zero.INSTA_USER, self.zero.INSTA_USER_ID))
        self.dbTool.inserttoTabel(self.dbConn, self.zero.DB_UPDATE_NEW_INSTA_DONE_TRUE, (self.zero.INSTA_USER_ID,))

    def runFollowScan(self):
        self.mainFunc.scanFollowToInstaID()
        input("+ Press [Enter] to continue...")

    def runLoadUserNodeScan(self):
        self.mainFunc.updateNodeFromList()

    def runEditDefault(self):
        self.sideTool.editDefaultValue()

    def runDeepfromDB(self):
        self.mainFunc.deepScanAll()

    def dispHelp(self):
        print(tabulate(self.zero.HELP_TEXT_TABLE, headers=self.zero.HELP_TEXT_TABLE_HEAD, tablefmt='grid'))
        print("")
        print(tabulate(self.zero.ERROR_TEXT_TABLE, headers=self.zero.ERROR_TEXT_TABLE_HEAD, tablefmt='grid'))
        input("\nPress [Enter] to continue...")

    def dispExport(self):
        self.mainFunc.exportDBData()
        input("+ Press [Enter] to continue...")

    def loginInstagram(self, instagram):
        #Iniatlaize Instagram login
        print("\n- Connecting to Instagram")
        self.instagram.with_credentials(self.zero.LOGIN_USERNAME_INSTA, self.zero.LOGIN_PASSWORD_INSTA, '/cachepath')
        self.instagram.login(force=False,two_step_verificator=True)
        sleep(2) # Delay to mimic user

    def root_path(self):
        return os.path.abspath(os.sep)

    def createFolder(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
            self.zero.printText("+ Folder created: {}".format(folder), True)
        else:
            self.zero.printText("+ Folder loacted: {}".format(folder), True)

    def createRootfolder(self):
        self.zero.OP_ROOT_FOLDER_PATH_VALUE = self.root_path()
        self.zero.OP_ROOT_FOLDER_PATH_VALUE = self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.OP_ROOT_FOLDER_NAME_VALUE
        self.createFolder(self.zero.OP_ROOT_FOLDER_PATH_VALUE)

        #Setup INSTA_FOLDER
        self.zero.OP_INSTA_FOLDER_NAME_VALUE =  self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.OP_INSTA_FOLDER_NAME_VALUE
        self.zero.OP_INSTA_PROFILEFOLDER_NAME_VALUE = self.zero.OP_INSTA_FOLDER_NAME_VALUE + self.zero.OP_INSTA_PROFILEFOLDER_NAME_VALUE
        self.zero.OP_INSTA_INSTAID_FOLDER_VALUE = self.zero.OP_INSTA_FOLDER_NAME_VALUE + self.zero.OP_INSTA_INSTAID_FOLDER_VALUE

        self.createFolder(self.zero.OP_INSTA_FOLDER_NAME_VALUE)
        self.createFolder(self.zero.OP_INSTA_PROFILEFOLDER_NAME_VALUE)
        self.createFolder(self.zero.OP_INSTA_INSTAID_FOLDER_VALUE)

        #Setting up full path starting
        self.zero.DB_DATABASE_FOLDER = self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.DB_DATABASE_FOLDER
        self.zero.DB_DATABASE_EXPORT_FOLDER = self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.DB_DATABASE_EXPORT_FOLDER
        self.zero.OP_ROOT_CONFIG = self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.OP_ROOT_CONFIG
        self.zero.printText("+ Database folder are loacted {}".format(self.zero.DB_DATABASE_FOLDER), False)
        self.zero.printText("+ Export folder are loacted {}".format(self.zero.DB_DATABASE_EXPORT_FOLDER), False)
        self.zero.printText("+ Config file are loacted {}".format(self.zero.OP_ROOT_CONFIG), False)

def run():
    #Run argv check
    try: offline = argv[1]
    except: offline = False

    if offline == "-o": offline = True
    else: offline = False

    myOptracker = Optracker(offline)
    while True:
        print("\n- Main menu")
        for item in myOptracker.MENU_ITEMS:
            print("[" + str(myOptracker.MENU_ITEMS.index(item)) + "] " + list(item.keys())[0])
        choice = input(">> ")

        if choice.isdigit():
            newInfo = int(choice)
            if newInfo <= len(myOptracker.MENU_ITEMS):
                list(myOptracker.MENU_ITEMS[newInfo].values())[0]()
            else:
                myOptracker.dispHelp()
        else:
            myOptracker.dispHelp()
