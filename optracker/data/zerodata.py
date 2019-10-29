import os
import json

class zerodata():
	#Define username and password
	LOGIN_USERNAME_INSTA = ""
	LOGIN_PASSWORD_INSTA = ""
	PROGRAM_NAME = "openSource Tracker v.1.2.7"

	#List log
	USER_FILES = (	["user_insta.txt"],
					["user_face.txt"],
					["user_list.txt"]
	)

	USER_FILE_SCAN_NODE_INSTA = "user_scan_insta.txt"

	#Menu variabels
	HELP_TEXT_DISP = "Display Help"
	RUN_CURRENT_DISP = "Singel Scan"
	RUN_FOLLOW_DISP = "Scan Followed by to user"
	RUN_CHANGE_USER = "Change user Instagram"
	RUN_EXPORT_DATA = "Export nodes and egdes"
	RUN_EDIT_OPTIONS = "Change default values"
	RUN_LOAD_SCAN = "Deepscan from list"
	RUN_GET_DEEP = "Deepscan from database"
	RUN_UPDATE_IMG = "Update Profile Images"
	RUN_EXIT_DISP = "Exit"

	#ERROR codes
	ERROR_429 = "429 - To many request"

	#FOLDER Setup
	OP_ROOT_FOLDER_PATH_TEXT = "OP_ROOT_FOLDER_PATH"
	OP_ROOT_FOLDER_PATH_VALUE = "/"

	OP_ROOT_FOLDER_NAME_TEXT = "OP_ROOT_FOLDER_NAME"
	OP_ROOT_FOLDER_NAME_VALUE = "optracker/"

	OP_INSTA_FOLDER_NAME_TEXT = "INSTA_FOLDER_NAME"
	OP_INSTA_FOLDER_NAME_VALUE = "instadata/"

	OP_INSTA_PROFILEFOLDER_NAME_TEXT = "INSTA_PROFILE_FOLDER_NAME"
	OP_INSTA_PROFILEFOLDER_NAME_VALUE = "profile_pic/"

	OP_INSTA_INSTAID_FOLDER_TEXT = "INSTA_INSTAID_FOLDER_NAME"
	OP_INSTA_INSTAID_FOLDER_VALUE = "post/"

	#Config filename
	OP_ROOT_CONFIG = "optracker.config"

	#Database setup
	DB_DATABASE = "openSource-tracker.db"
	DB_DATABASE_FOLDER = "db/"
	DB_DATABASE_EXPORT_FOLDER = "export/"
	DB_DATABASE_EXPORT_NODES = "nodes.csv"
	DB_DATABASE_EXPORT_INSTA_EGDE = "edges_insta.csv"

	#DB MYSQL
	DB_MYSQL = "localhost"
	DB_MYSQL_USER = "optracker"
	DB_MYSQL_PASSWORD = "localpassword"
	DB_MYSQL_DATABASE = "openSource_tracker"
	DB_MYSQL_PORT = "3306"
	DB_MYSQL_ON = 0
	DB_MYSQL_COLLATION = "utf8mb4_general_ci"
	DB_MYSQL_CHARSET = "utf8mb4"

	DB_MYSQL_TEXT = "MYSQL_HOST"
	DB_MYSQL_USER_TEXT = "MYSQL_USER"
	DB_MYSQL_PASSWORD_TEXT = "MYSQL_PASSWORD"
	DB_MYSQL_DATABASE_TEXT = "MYSQL_DB"
	DB_MYSQL_PORT_TEXT = "MYSQL_PORT"
	DB_MYSQL_ON_TEXT = "MYSQL_ON"
	DB_MYSQL_COLLATION_TEXT = "MYSQL_COL"
	DB_MYSQL_CHARSET_TEXT = "MYSQL_CHAR"

	#SQLIte
	DB_TABLE_NODES = """
	CREATE TABLE IF NOT EXISTS "nodes" (
		"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
		"name"	TEXT,
		"label"	TEXT,
		"insta_id"	INTEGER,
		"insta_img"	TEXT,
		"insta_follow"	INTEGER,
		"insta_follower"	INTEGER,
		"insta_bio"	TEXT,
		"insta_username"	TEXT,
		"insta_private"	INTEGER,
		"insta_verifyed"	INTEGER,
		"insta_post"	INTEGER,
		"insta_exturl"	TEXT,
		"insta_deepscan"	INTEGER DEFAULT 0
		);"""

	DB_TABLE_EGDES = """
	CREATE TABLE IF NOT EXISTS "egdes_insta" (
		"source"	INTEGER,
		"target"	INTEGER,
		"type"	TEXT DEFAULT 'undirected',
		"weight"	INTEGER DEFAULT 1
	);"""

	DB_TABLE_NEW_INSTA = """
	CREATE TABLE IF NOT EXISTS "new_insta" (
		"insta_id"	INTEGER UNIQUE,
		"insta_user"	INTEGER,
		"done"	INTEGER DEFAULT 0,
		"wait"	INTEGER DEFAULT 0,
		"followed_by_done"	INTEGER DEFAULT 0
	);
	"""

	DB_TABLE_LOGIN_INSTA = """
	CREATE TABLE IF NOT EXISTS "accounts" (
		"username"	TEXT UNIQUE,
		"password"	TEXT,
		"email"	TEXT,
		"fullname"	TEXT,
		"account_type"	TEXT,
		"current_run"	INTEGER DEFAULT 0,
		"last_used"	TEXT
	);
	"""

	DB_TABLE_OPTIONS = """
	CREATE TABLE IF NOT EXISTS "options" (
	"what"	TEXT UNIQUE,
	"value"	TEXT,
	"ref"	TEXT
	);
	"""

	#MYSQL
	DB_TABLE_MYSQL_NODES = """
	CREATE TABLE IF NOT EXISTS nodes (
		id BIGINT(20) NOT NULL AUTO_INCREMENT,
		name VARCHAR(64) NULL DEFAULT "N/A",
		label VARCHAR(64) NULL DEFAULT "N/A",
		insta_id BIGINT(20) NULL DEFAULT 0,
		insta_img TEXT NULL,
		insta_follow BIGINT(20) NULL DEFAULT 0,
		insta_follower BIGINT(20) NOT NULL DEFAULT 0,
		insta_bio TEXT NULL,
		insta_username VARCHAR(64) NOT NULL DEFAULT "N/A",
		insta_private INT(10) NOT NULL DEFAULT 0,
		insta_verifyed INT(10) NOT NULL DEFAULT 0,
		insta_post BIGINT(20) NOT NULL DEFAULT 0,
		insta_exturl TEXT NULL,
		insta_deepscan INT(20) NOT NULL DEFAULT '0',
		PRIMARY KEY (`id`)) ENGINE = MyISAM
	"""

	DB_TABLE_MYSQL_EGDES = """
	CREATE TABLE IF NOT EXISTS egdes_insta (
	source BIGINT(20) NOT NULL ,
	target BIGINT(20) NOT NULL ,
	type VARCHAR(64) NOT NULL DEFAULT 'undirected' ,
	weight INT(20) NOT NULL DEFAULT '1'
	) ENGINE = MyISAM;"""

	DB_TABLE_MYSQL_NEW_INSTA = """
	CREATE TABLE IF NOT EXISTS new_insta (
		insta_id			BIGINT(20) NOT NULL UNIQUE,
		insta_user			TEXT NULL,
		done				INT(20) NOT NULL DEFAULT 0,
		wait				INT(20) NOT NULL DEFAULT 0,
		followed_by_done	INT(20) NOT NULL DEFAULT 0
	) ENGINE = MyISAM;
	"""

	DB_TABLE_MYSQL_LOGIN_INSTA = """
	CREATE TABLE IF NOT EXISTS accounts (
		username	VARCHAR(64) NOT NULL UNIQUE,
		password	VARCHAR(64) NOT NULL,
		email		VARCHAR(64) NOT NULL,
		fullname	VARCHAR(64) NOT NULL,
		account_type	VARCHAR(64) NOT NULL,
		current_run	INT(20) NOT NULL DEFAULT 0,
		last_used	VARCHAR(64) NOT NULL DEFAULT 0
	) ENGINE = MyISAM;"""

	DB_TABLE_MYSQL_OPTIONS = """
	CREATE TABLE IF NOT EXISTS options (
		what	VARCHAR(64) NOT NULL UNIQUE,
		value	VARCHAR(64) NOT NULL,
		ref		VARCHAR(64) NOT NULL DEFAULT 0
	) ENGINE = MyISAM;
	"""

	#MySQL
	DB_INSERT_MYSQL_NODE = """INSERT INTO nodes (name, label, insta_id, insta_img, insta_follow, insta_follower, insta_bio, insta_username, insta_private, insta_verifyed, insta_post, insta_exturl, insta_deepscan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); SELECT id FROM nodes where insta_id = %s;"""
	DB_INSERT_MYSQL_INSTA_EGDE = 'INSERT INTO egdes_insta (source, target) VALUES (%s, %s);'
	DB_INSERT_MYSQL_NEW_INSTA = 'INSERT INTO new_insta (insta_id, insta_user) VALUES (%s, %s);'
	DB_INSERT_MYSQL_LOGIN_INSTA = 'INSERT INTO accounts (username, password, email, fullname, account_type, last_used) VALUES (%s, %s, %s, %s, %s, %s);'
	DB_INSERT_MYSQL_OPTIONS_LASTINSTA = 'INSERT INTO options (value, what) VALUES (%s, %s);'
	DB_SELECT_MYSQL_DEEPSCAN_NEED = 'SELECT insta_username FROM nodes WHERE insta_deepscan = 0'

	DB_UPDATE_MYSQL_LAST_INSTA = 'UPDATE options SET value = (%s) WHERE what = "LAST_INSTA";'
	DB_UPDATE_MYSQL_OPTIONS = 'UPDATE options SET value = (%s) WHERE what = %s;'
	DB_UPDATE_MYSQL_NEW_INSTA_DONE_TRUE = 'UPDATE new_insta SET done = 1 WHERE insta_id = %s;'
	DB_UPDATE_MYSQL_NEW_INSTA_DONE_FALSE = 'UPDATE new_insta SET done = 0 WHERE insta_id = %s;'
	DB_UPDATE_MYSQL_ACCOUNT_LAST_USED = 'UPDATE accounts SET last_used = %s WHERE username = %s'
	DB_UPDATE_MYSQL_NODES = 'UPDATE nodes SET name = %s, label = %s, insta_img = %s, insta_follow = %s, insta_follower = %s, insta_bio = %s, insta_username = %s, insta_private = %s, insta_verifyed = %s, insta_post = %s, insta_exturl = %s, insta_deepscan = %s WHERE insta_id = %s'

	DB_SELECT_MYSQL_IMG = 'SELECT insta_username, insta_id, insta_img FROM nodes WHERE insta_img IS NOT NULL AND insta_img IS NOT "None"'
	DB_SELECT_MYSQL_EXPORT_ID_USER = 'SELECT id, insta_username FROM nodes'
	DB_SELECT_MYSQL_ID_NODE = 'SELECT id FROM nodes WHERE insta_id = %s'
	DB_SELECT_MYSQL_USERNAME_NODE = 'SELECT insta_username FROM nodes WHERE insta_id = %s'
	DB_SELECT_MYSQL_DONE_NEW_INSTA = 'SELECT done, wait FROM new_insta WHERE insta_id = %s'
	DB_SELECT_MYSQL_TARGET_EDGE = 'SELECT target FROM egdes_insta WHERE source = %s AND target = %s'
	DB_SELECT_MYSQL_LOGIN_INSTA = 'SELECT * FROM accounts WHERE account_type = "instagram"'
	DB_SELECT_MYSQL_LOGIN_PASSWORD_INSTA = 'SELECT password FROM accounts WHERE username = %s AND account_type = "instagram"'
	DB_SELECT_MYSQL_OPTIONS = 'SELECT * FROM options WHERE what = %s'
	DB_SELECT_MYSQL_ALL_DONE_NEW_INSTA = 'SELECT * FROM new_insta WHERE done = 1'
	DB_SELECT_MYSQL_ALL_NODE = "SELECT * FROM nodes"
	DB_SELECT_MYSQL_ALL_INSTA_EDGES = "SELECT source, target, type, weight FROM egdes_insta"
	DB_SELECT_MYSQL_COUNT_NODES = "SELECT count(*) FROM nodes"
	DB_SELECT_MYSQL_COUNT_EDES_INSTA = "SELECT count(*) FROM egdes_insta"
	DB_SELECT_MYSQL_INSTA_FOLLOWER_NODE_ID = 'SELECT insta_follower FROM nodes WHERE id = %s'
	DB_SELECT_MYSQL_FOLLOW_OF = 'SELECT * FROM nodes as Node INNER JOIN egdes_insta as Edge ON Node.id = Edge.source WHERE Node.insta_private = 0 AND Edge.target = %s'


	#SQLite
	DB_SELECT_EXPORT_ID_USER = 'SELECT id, insta_username FROM nodes'
	DB_INSERT_NODE = """INSERT INTO "main"."nodes" ("name", "label", "insta_id", "insta_img", "insta_follow", "insta_follower", "insta_bio", "insta_username", "insta_private", "insta_verifyed", "insta_post", "insta_exturl", "insta_deepscan") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); SELECT id FROM nodes where insta_id = ?;"""
	DB_INSERT_INSTA_EGDE = 'INSERT INTO "main"."egdes_insta" ("source", "target") VALUES (?, ?);'
	DB_INSERT_NEW_INSTA = 'INSERT INTO "main"."new_insta" ("insta_id", "insta_user") VALUES (?, ?);'
	DB_INSERT_LOGIN_INSTA = 'INSERT INTO "main"."accounts" ("username", "password", "email", "fullname", "account_type", "last_used") VALUES (?, ?, ?, ?, ?, ?);'
	DB_INSERT_OPTIONS_LASTINSTA = 'INSERT INTO "main"."options" ("value", "what") VALUES (?, ?);'

	DB_UPDATE_LAST_INSTA = 'UPDATE "main"."options" SET "value" = (?) WHERE "what" = "LAST_INSTA";'
	DB_UPDATE_OPTIONS = 'UPDATE "main"."options" SET "value" = (?) WHERE "what" = ?;'
	DB_UPDATE_NEW_INSTA_DONE_TRUE = 'UPDATE "main"."new_insta" SET "done" = 1 WHERE "insta_id" = ?;'
	DB_UPDATE_NEW_INSTA_DONE_FALSE = 'UPDATE "main"."new_insta" SET "done" = 0 WHERE "insta_id" = ?;'
	DB_UPDATE_ACCOUNT_LAST_USED = 'UPDATE "main"."accounts" SET ("last_used") = ? WHERE username = ?'
	DB_UPDATE_NODES = 'UPDATE "main"."nodes" SET "name" = ?, "label" = ?, "insta_img" = ?, "insta_follow" = ?, "insta_follower" = ?, "insta_bio" = ?, "insta_username" = ?, "insta_private" = ?, "insta_verifyed" = ?, "insta_post" = ?, "insta_exturl" = ?, "insta_deepscan" = ? WHERE "insta_id" = ?'

	DB_SELECT_IMG = 'SELECT insta_username, insta_id, insta_img FROM nodes WHERE insta_img IS NOT NULL AND insta_img IS NOT "None"'
	DB_SELECT_DEEPSCAN_NEED = 'SELECT insta_username FROM nodes WHERE insta_deepscan = 0'
	DB_SELECT_ID_NODE = 'SELECT id FROM "main"."nodes" WHERE ("insta_id") = ?'
	DB_SELECT_USERNAME_NODE = 'SELECT insta_username FROM "main"."nodes" WHERE insta_id = ?'
	DB_SELECT_DONE_NEW_INSTA = 'SELECT done, wait FROM "main"."new_insta" WHERE ("insta_id") = ?'
	DB_SELECT_TARGET_EDGE = 'SELECT target FROM "main"."egdes_insta" WHERE source = ? AND target = ?'
	DB_SELECT_LOGIN_INSTA = 'SELECT * FROM "main"."accounts" WHERE account_type = "instagram"'
	DB_SELECT_LOGIN_PASSWORD_INSTA = 'SELECT password FROM "main"."accounts" WHERE ("username") = ? AND account_type = "instagram"'
	DB_SELECT_OPTIONS = 'SELECT * FROM options WHERE what = ?'
	DB_SELECT_ALL_DONE_NEW_INSTA = 'SELECT * FROM "main"."new_insta" WHERE done = 1'
	DB_SELECT_ALL_NODE = "SELECT * FROM main.nodes"
	DB_SELECT_ALL_INSTA_EDGES = "SELECT source, target, type, weight FROM main.egdes_insta"
	DB_SELECT_COUNT_NODES = "SELECT count(*) FROM main.nodes"
	DB_SELECT_COUNT_EDES_INSTA = "SELECT count(*) FROM main.egdes_insta"
	DB_SELECT_INSTA_FOLLOWER_NODE_ID = 'SELECT insta_follower FROM "main"."nodes" WHERE id = ?'
	DB_SELECT_FOLLOW_OF = 'SELECT * FROM "main"."nodes" as Node INNER JOIN "main"."egdes_insta" as Edge ON Node.id = Edge.source WHERE Node.insta_private = 0 AND Edge.target = ?'


	#Startpoint information
	INSTA_USER = ""
	INSTA_USER_ID = ""
	INSERT_DATA = ""
	DATETIME_MASK = "%Y-%m-%d %H:%M:%S.%f"
	TOTAL_USER_COUNT = 0
	WRITE_ENCODING = "utf-8"
	ON_ERROR_ENCODING = "replace"
	INSTA_FILE_EXT = ".jpg"

	INSTA_MAX_FOLLOW_SCAN_TEXT = "INSTA_MAX_FOLLOW_SCAN"
	INSTA_MAX_FOLLOW_SCAN_VALUE = 2000

	INSTA_MAX_FOLLOW_BY_SCAN_TEXT = "INSTA_MAX_FOLLOW_BY_SCAN"
	INSTA_MAX_FOLLOW_BY_SCAN_VALUE = 2000

	SURFACE_SCAN_TEXT = "SURFACE_SCAN"
	SURFACE_SCAN_VALUE = "1"

	DETAIL_PRINT_TEXT = "DETAIL_PRINT"
	DETAIL_PRINT_VALUE = "1"

	LAST_INSTA_TEXT = "LAST_INSTA"
	LAST_INSTA_VALUE = ""

	DOWNLOAD_PROFILE_INSTA_TEXT = "DOWNLOAD_PROFILE_INSTA"
	DOWNLOAD_PROFILE_INSTA_VALUE = "1"


	#Help TEXT
	HELP_TEXT = """
	{} - HELP TEXT

	{} - Scan a specific node
		This mode will allow you to run a scan for a specific user and is your first step to generate nodes and edges. You will need to enter a startpoint, it is a instagram username. The program will look it up find follow and followed by. For then to add it to the database with connections.

	{} - Scan all follower
		You will be presented with a list of users that you have finnished adding to your database. The program til then scan all the connections it has as it was a first time use and add the data to the database. Short and sweet scan the follow to the follow for a user.

	{} - Allow you to change users
		This will give you a list of all avalible users so you can change before the scan if you are not happy with the choice from startup.

	Nodes - Main database
		The node database is a collection of all the users that have been scanned. It contains basic data as ID, username, instagram description with more.

	Edges - connections
		The edges database is a database with connections between nodes. This is used to create a visual display for how a social nettwork are connected.

	SQLite - The Database
		All data are saved in the database found in folder 'db/'. You need to open it in a SQL browser and then export the data in node table and edges table to a .CSV file witch you can import into a visualising program (eks. gephi).

	{} - RUN_EXPORT_DATA
		Gives you an overveiew of data collected so far, and exports it to folder {}.

	{}
		Loads a list of users from root folder, scraps all info from instagram and updates node DB.

	Max Follows and Max Followed by
		During search of follows by, where you scan the profile for one user that have completet the singel search you can set a limit to how many followers a user can have or how many it are following. This is to prevent to scan uninterested profils like public organizations and so on as they can have up to 10K. Default is 2000 and is considerated a normal amount of followes/followed by.

	Deepscan and Surfacescan
		On default are SurfaceScan turned off. By turning on surfacescan you only extract username and instagram id when scraping. This is to save you for request to the server so you can use one user for a longer periode of time, and make the scan go quicker if you are scraping a big nettwork. You can later add specific users found in the graphic to a text file and scan only the ones that are interesting and get all the data.

	Print Detail
		On Default is it turned ON. You will be presented with all the output the scraper have. If turned OFF you will only get the minimum of info to see if it is working properly.

	ERROR CODES - List of ERROR codes
		001 - INSTAGRAM USER BLOCKED
		002 - TO MANY REQUEST FROM CURRENT USER
		003 - ERROR LOGIN
		004 - USER DONT HAVE ACCESS TO DATA, RETURNING JSON ERROR
		""".format(PROGRAM_NAME, RUN_CURRENT_DISP, RUN_FOLLOW_DISP, RUN_CHANGE_USER, RUN_EXPORT_DATA, DB_DATABASE_EXPORT_FOLDER, RUN_LOAD_SCAN)


	def printText(self, text, override):
		if int(self.DETAIL_PRINT_VALUE) == 1:
			print(text)
		else:
			if override == True:
				print(text)

	#Removes unwanted symbols in string
	def sanTuple(self, text):
		text = str(text)
		text = text.replace("'", "")
		text = text.replace('"', "")
		text = text.replace(";", "")

		return text

	def setupJSON(self, export):
		if export == True:
			self.printText("+ Config export started", False)
			DATA = {}
			DATA['DB'] = []
			DATA['DB'].append({
				self.DB_MYSQL_TEXT : self.DB_MYSQL,
				self.DB_MYSQL_USER_TEXT : self.DB_MYSQL_USER,
				self.DB_MYSQL_PASSWORD_TEXT : self.DB_MYSQL_PASSWORD,
				self.DB_MYSQL_DATABASE_TEXT : self.DB_MYSQL_DATABASE,
				self.DB_MYSQL_PORT_TEXT : self.DB_MYSQL_PORT,
				self.DB_MYSQL_ON_TEXT : self.DB_MYSQL_ON,
				self.DB_MYSQL_COLLATION_TEXT : self.DB_MYSQL_COLLATION,
				self.DB_MYSQL_CHARSET_TEXT : self.DB_MYSQL_CHARSET,
				self.DETAIL_PRINT_TEXT : self.DETAIL_PRINT_VALUE
			})

			if os.path.exists(self.OP_ROOT_CONFIG):
				self.printText("+ File: {} exist, deleting it.".format(self.OP_ROOT_CONFIG), False)
				os.remove(self.OP_ROOT_CONFIG)

			with open(self.OP_ROOT_CONFIG, 'w') as outfile:
				json.dump(DATA, outfile)

			self.printText("+ Config export end", False)

		else:
			self.printText("+ Config import started", True)
			if os.path.exists(self.OP_ROOT_CONFIG):
				with open(self.OP_ROOT_CONFIG) as json_file:
					data = json.load(json_file)
					for p in data['DB']:
						self.DB_MYSQL = p[self.DB_MYSQL_TEXT]
						self.DB_MYSQL_USER = p[self.DB_MYSQL_USER_TEXT]
						self.DB_MYSQL_PASSWORD = p[self.DB_MYSQL_PASSWORD_TEXT]
						self.DB_MYSQL_DATABASE = p[self.DB_MYSQL_DATABASE_TEXT]
						self.DB_MYSQL_PORT = int(p[self.DB_MYSQL_PORT_TEXT])
						self.DB_MYSQL_ON = int(p[self.DB_MYSQL_ON_TEXT])
						self.DB_MYSQL_COLLATION = p[self.DB_MYSQL_COLLATION_TEXT]
						self.DB_MYSQL_CHARSET = p[self.DB_MYSQL_CHARSET_TEXT]
						self.DETAIL_PRINT_VALUE = int(p[self.DETAIL_PRINT_TEXT])

						self.printText("+ {} are set to: {}".format(self.DB_MYSQL_TEXT, self.DB_MYSQL), False)
						self.printText("+ {} are set to: {}".format(self.DB_MYSQL_USER_TEXT, self.DB_MYSQL_USER), False)
						self.printText("+ {} are set to: {}".format(self.DB_MYSQL_PASSWORD_TEXT, self.DB_MYSQL_PASSWORD), False)
						self.printText("+ {} are set to: {}".format(self.DB_MYSQL_DATABASE_TEXT, self.DB_MYSQL_DATABASE), False)
						self.printText("+ {} are set to: {}".format(self.DB_MYSQL_PORT_TEXT, self.DB_MYSQL_PORT), False)
						self.printText("+ {} are set to: {}".format(self.DB_MYSQL_ON_TEXT, self.DB_MYSQL_ON), False)
						self.printText("+ {} are set to: {}".format(self.DB_MYSQL_COLLATION_TEXT, self.DB_MYSQL_COLLATION), False)
						self.printText("+ {} are set to: {}".format(self.DB_MYSQL_CHARSET_TEXT, self.DB_MYSQL_CHARSET), False)
						self.printText("+ {} are set to: {}".format(self.DETAIL_PRINT_TEXT, self.DETAIL_PRINT_VALUE), False)

			else:
				self.printText("+ Config file dosent exist - using standard", False)

			self.changeSQLquery()
			self.printText("+ Config import end", False)

	def changeSQLquery(self):
		if self.DB_MYSQL_ON == 1:
			self.DB_INSERT_NODE = self.DB_INSERT_MYSQL_NODE
			self.DB_INSERT_INSTA_EGDE = self.DB_INSERT_MYSQL_INSTA_EGDE
			self.DB_INSERT_NEW_INSTA = self.DB_INSERT_MYSQL_NEW_INSTA
			self.DB_INSERT_LOGIN_INSTA = self.DB_INSERT_MYSQL_LOGIN_INSTA
			self.DB_INSERT_OPTIONS_LASTINSTA = self.DB_INSERT_MYSQL_OPTIONS_LASTINSTA
			self.DB_UPDATE_LAST_INSTA = self.DB_UPDATE_MYSQL_LAST_INSTA
			self.DB_UPDATE_OPTIONS = self.DB_UPDATE_MYSQL_OPTIONS
			self.DB_UPDATE_NEW_INSTA_DONE_TRUE = self.DB_UPDATE_MYSQL_NEW_INSTA_DONE_TRUE
			self.DB_UPDATE_NEW_INSTA_DONE_FALSE = self.DB_UPDATE_MYSQL_NEW_INSTA_DONE_FALSE
			self.DB_UPDATE_ACCOUNT_LAST_USED = self.DB_UPDATE_MYSQL_ACCOUNT_LAST_USED
			self.DB_UPDATE_NODES = self.DB_UPDATE_MYSQL_NODES
			self.DB_SELECT_ID_NODE = self.DB_SELECT_MYSQL_ID_NODE
			self.DB_SELECT_USERNAME_NODE = self.DB_SELECT_MYSQL_USERNAME_NODE
			self.DB_SELECT_DONE_NEW_INSTA = self.DB_SELECT_MYSQL_DONE_NEW_INSTA
			self.DB_SELECT_TARGET_EDGE = self.DB_SELECT_MYSQL_TARGET_EDGE
			self.DB_SELECT_LOGIN_INSTA = self.DB_SELECT_MYSQL_LOGIN_INSTA
			self.DB_SELECT_LOGIN_PASSWORD_INSTA = self.DB_SELECT_MYSQL_LOGIN_PASSWORD_INSTA
			self.DB_SELECT_OPTIONS = self.DB_SELECT_MYSQL_OPTIONS
			self.DB_SELECT_ALL_DONE_NEW_INSTA = self.DB_SELECT_MYSQL_ALL_DONE_NEW_INSTA
			self.DB_SELECT_ALL_NODE = self.DB_SELECT_MYSQL_ALL_NODE
			self.DB_SELECT_ALL_INSTA_EDGES = self.DB_SELECT_MYSQL_ALL_INSTA_EDGES
			self.DB_SELECT_COUNT_NODES = self.DB_SELECT_MYSQL_COUNT_NODES
			self.DB_SELECT_COUNT_EDES_INSTA = self.DB_SELECT_MYSQL_COUNT_EDES_INSTA
			self.DB_SELECT_INSTA_FOLLOWER_NODE_ID = self.DB_SELECT_MYSQL_INSTA_FOLLOWER_NODE_ID
			self.DB_SELECT_FOLLOW_OF = self.DB_SELECT_MYSQL_FOLLOW_OF
			self.DB_SELECT_DEEPSCAN_NEED = self.DB_SELECT_MYSQL_DEEPSCAN_NEED
			self.DB_SELECT_EXPORT_ID_USER = self.DB_SELECT_MYSQL_EXPORT_ID_USER
			self.DB_SELECT_IMG = self.DB_SELECT_MSQL_IMG

	def __init__(self):
		#Starting up
		print("- Starting {}".format(self.PROGRAM_NAME))
		print("+ Text Libray loaded")
