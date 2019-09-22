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

#Starting up
print("- Starting openSource Tracker v.0.1")

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

#Setup zeroPoint
sideTool.lastSearch()
mainFunc.setCurrentUser(zerodata.INSTA_USER)

#Extract info from following list
#mainFunc.loadFollowlist(False)
#mainFunc.add_egde_from_list_insta(False)

#Extract followed by
mainFunc.loadFollowlist(True)
mainFunc.add_egde_from_list_insta(True)

"""
try:
except KeyboardInterrupt:
        print('CTRL+C received... shutting down')
"""

#Clean up
dbConn.close()
