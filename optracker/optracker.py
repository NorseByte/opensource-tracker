import os
from .data.zerodata import zerodata
from .functions.db_func import *
from .functions.side_func import *
from .functions.core_func import *
from .igramscraper.instagram import Instagram
from time import sleep

class Optracker():
    def __init__(self):
        #Adding Text source
        self.zero = zerodata()

        #Setting up OP_ROOT_FOLDER
        self.createRootfolder()

        #Load Config
        self.zero.setupJSON(False)

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
        else:
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_NODES)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_EGDES)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_NEW_INSTA)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_LOGIN_INSTA)
            self.dbTool.createTabels(self.dbConn, self.zero.DB_TABLE_MYSQL_OPTIONS)

        self.dbTool.setDefaultValueOptions(self.dbConn)
        self.zero.printText("+ DB setup complete", False)

        #Get usernames
        self.sideTool = sideFunc(self.dbTool, self.dbConn, self.zero)
        self.sideTool.loadLoginText()
        self.sideTool.countCurrentUser()

        #Init INSTAGRAM
        self.instagram = Instagram()

        #User Select and Login
        #selectUserAndLogin()
        self.autoSelectAndLogin()

        #Setup coreFunc
        print("+ Setting up core functions")
        self.mainFunc = coreFunc(self.dbTool, self.dbConn, self.instagram, self.zero)

        self.MENU_ITEMS = [
            { self.zero.HELP_TEXT_DISP: self.dispHelp },
            { self.zero.RUN_CURRENT_DISP: self.runSingelScan },
            { self.zero.RUN_FOLLOW_DISP: self.runFollowScan },
            { self.zero.RUN_CHANGE_USER: self.selectUserAndLogin },
            { self.zero.RUN_LOAD_SCAN: self.runLoadUserNodeScan },
            { self.zero.RUN_EXPORT_DATA: self.dispExport},
            { self.zero.RUN_EDIT_OPTIONS: self.runEditDefault},
            { self.zero.RUN_GET_DEEP: self.runDeepfromDB},
            { self.zero.RUN_EXIT_DISP: exit},
        ]

    #Core Functions to main
    def runSingelScan(self):
        #Setup zeroPoint
        self.sideTool.lastSearch()

        #Run Scan from zeroPoint
        self.mainFunc.setCurrentUser(self.zero.INSTA_USER)
        self.runCurrentScan()

    def dbSelect(self):
        print("+ Selecting DB")

    def selectUserAndLogin(self):
        #Setusername
        self.sideTool.setupLogin()
        #Login Instagram
        self.loginInstagram(instagram)

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
        print(self.zero.HELP_TEXT)
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

    def createRootfolder(self):
        self.zero.OP_ROOT_FOLDER_PATH_VALUE = self.root_path()
        currentFolder = self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.OP_ROOT_FOLDER_NAME_VALUE
        self.zero.OP_ROOT_FOLDER_PATH_VALUE = currentFolder

        if not os.path.exists(currentFolder):
            os.mkdir(currentFolder)
            self.zero.printText("+ Root folder created at: {}".format(self.zero.OP_ROOT_FOLDER_PATH_VALUE), True)

        else:
            self.zero.printText("+ Root folder located at: {}".format(self.zero.OP_ROOT_FOLDER_PATH_VALUE), True)

        #Setting up full path starting
        self.zero.DB_DATABASE_FOLDER = self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.DB_DATABASE_FOLDER
        self.zero.DB_DATABASE_EXPORT_FOLDER = self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.DB_DATABASE_EXPORT_FOLDER
        self.zero.OP_ROOT_CONFIG = self.zero.OP_ROOT_FOLDER_PATH_VALUE + self.zero.OP_ROOT_CONFIG
        self.zero.printText("+ Database folder are loacted {}".format(self.zero.DB_DATABASE_FOLDER), False)
        self.zero.printText("+ Export folder are loacted {}".format(self.zero.DB_DATABASE_EXPORT_FOLDER), False)
        self.zero.printText("+ Config file are loacted {}".format(self.zero.OP_ROOT_CONFIG), False)

def run():
    myOptracker = Optracker()
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
