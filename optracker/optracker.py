'''
openSource tracker v.0.1
by Marcus Knoph

Used in bachlor to test theory, and prove possibilitys.
'''

import os
import zerodata
from time import sleep
from functions.db_func import *
from functions.core_func import *
from functions.side_func import *
from context import Instagram

#Core Functions to main
def runSingelScan():
    #Setup zeroPoint
    sideTool.lastSearch()
    mainFunc.setCurrentUser(zerodata.INSTA_USER)

    #rRun Scan
    runCurrentScan()

def runCurrentScan():
    #Extract info from following list
    mainFunc.loadFollowlist(False)
    mainFunc.add_egde_from_list_insta(False)

    #Extract followed by
    mainFunc.loadFollowlist(True)
    mainFunc.add_egde_from_list_insta(True)

    #Update new_Insta
    print("\n- Scan complete")
    print("+ Setting {} ({}) to complete.".format(zerodata.INSTA_USER, zerodata.INSTA_USER_ID))
    dbTool.inserttoTabel(dbConn, zerodata.DB_UPDATE_NEW_INSTA_DONE_TRUE, (zerodata.INSTA_USER_ID,))

def runFollowScan():
    print("Follow Scan")
    input("Press [Enter] to continue...")

def dispHelp():
    print(zerodata.HELP_TEXT)
    input("\nPress [Enter] to continue...")

MENU_ITEMS = [
    { zerodata.HELP_TEXT_DISP: dispHelp },
    { zerodata.RUN_CURRENT_DISP: runSingelScan },
    { zerodata.RUN_FOLLOW_DISP: runFollowScan },
	{ zerodata.RUN_EXIT_DISP: exit},
]

try:
    #Starting up
    print("- Starting {}".format(zerodata.PROGRAM_NAME))

    #Iniatlaize DB_DATABASE
    print("+ Setting up DB")
    dbTool = dbFunc(zerodata.DB_DATABASE)
    dbConn =  dbTool.create_connection()
    dbTool.createTabels(dbConn, zerodata.DB_TABLE_NODES)
    dbTool.createTabels(dbConn, zerodata.DB_TABLE_EGDES)
    dbTool.createTabels(dbConn, zerodata.DB_TABLE_NEW_INSTA)
    dbTool.createTabels(dbConn, zerodata.DB_TABLE_LOGIN_INSTA)
    print("+ DB setup complete")

    #Get usernames
    sideTool = sideFunc(dbTool, dbConn)
    sideTool.loadLoginText()
    sideTool.setupLogin()

    #Iniatlaize Instagram login
    print("\n- Connecting to Instagram")
    instagram = Instagram()
    instagram.with_credentials(zerodata.LOGIN_USERNAME_INSTA, zerodata.LOGIN_PASSWORD_INSTA, '/cachepath')
    instagram.login(force=False,two_step_verificator=True)
    sleep(2) # Delay to mimic user
    print("+ Connected to Instagram with user:", zerodata.LOGIN_USERNAME_INSTA)

    #Setup coreFunc
    print("+ Setting up core functions")
    mainFunc = coreFunc(dbTool, dbConn, instagram)

    #Print meny and innput
    while True:
        print("\n- Main menu")
        for item in MENU_ITEMS:
            print("[" + str(MENU_ITEMS.index(item)) + "] " + list(item.keys())[0])
        choice = input(">> ")
        try:
            if int(choice) < 0 : raise ValueError
            list(MENU_ITEMS[int(choice)].values())[0]() # Call the matching function
        except (ValueError, IndexError):
            dispHelp()

except KeyboardInterrupt:
        print('\n\n- CTRL+C received... shutting down')

#Clean up
dbConn.close()
