import os

class zerodata():
	#Define username and password
	LOGIN_USERNAME_INSTA = ""
	LOGIN_PASSWORD_INSTA = ""
	PROGRAM_NAME = "openSource Tracker v.1.0.0"

	#List log
	USER_FILES = (	["user_insta.txt"],
					["user_face.txt"],
					["user_list.txt"]
	)

	#Menu variabels
	HELP_TEXT_DISP = "Display Help"
	RUN_CURRENT_DISP = "Singel Scan"
	RUN_FOLLOW_DISP = "Scan Followed by to user"
	RUN_CHANGE_USER = "Change user Instagram"
	RUN_EXPORT_DATA = "Export nodes and egdes"
	RUN_EDIT_OPTIONS = "Change default values"
	RUN_EXIT_DISP = "Exit"


	#ERROR codes
	ERROR_429 = "429 - To many request"

	#FOLDER Setup
	OP_ROOT_FOLDER_PATH_TEXT = "OP_ROOT_FOLDER_PATH"
	OP_ROOT_FOLDER_PATH_VALUE = "/"

	OP_ROOT_FOLDER_NAME_TEXT = "OP_ROOT_FOLDER_NAME"
	OP_ROOT_FOLDER_NAME_VALUE = "optracker/"

	#Database setup
	DB_DATABASE = "openSource-tracker.db"
	DB_DATABASE_FOLDER = "db/"
	DB_DATABASE_EXPORT_FOLDER = "export/"
	DB_DATABASE_EXPORT_NODES = "nodes.csv"
	DB_DATABASE_EXPORT_INSTA_EGDE = "edges_insta.csv"

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
		"what"	INTEGER UNIQUE,
		"value"	INTEGER,
		"ref"	INTEGER
	);
	"""

	DB_INSERT_NODE = """
	INSERT INTO "main"."nodes"
	("name", "label", "insta_id", "insta_img", "insta_follow", "insta_follower", "insta_bio", "insta_username", "insta_private", "insta_verifyed", "insta_post", "insta_exturl", "insta_deepscan")
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
	"""

	DB_INSERT_INSTA_EGDE = 'INSERT INTO "main"."egdes_insta" ("source", "target") VALUES (?, ?);'
	DB_INSERT_NEW_INSTA = 'INSERT INTO "main"."new_insta" ("insta_id", "insta_user") VALUES (?, ?);'
	DB_INSERT_LOGIN_INSTA = 'INSERT INTO "main"."accounts" ("username", "password", "email", "fullname", "account_type") VALUES (?, ?, ?, ?, ?);'
	DB_INSERT_OPTIONS_LASTINSTA = 'INSERT INTO "main"."options" ("value", "what") VALUES (?, ?);'

	DB_UPDATE_LAST_INSTA = 'UPDATE "main"."options" SET "value" = (?) WHERE "what" = "last_insta";'
	DB_UPDATE_OPTIONS = 'UPDATE "main"."options" SET "value" = (?) WHERE "what" = ?;'
	DB_UPDATE_NEW_INSTA_DONE_TRUE = 'UPDATE "main"."new_insta" SET "done" = 1 WHERE "insta_id" = ?;'
	DB_UPDATE_NEW_INSTA_DONE_FALSE = 'UPDATE "main"."new_insta" SET "done" = 0 WHERE "insta_id" = ?;'
	DB_UPDATE_ACCOUNT_LAST_USED = 'UPDATE "main"."accounts" SET ("last_used") = ? WHERE username = ?'
	DB_UPDATE_NODES = 'UPDATE "main"."nodes" SET "name" = ?, "label" = ?, "insta_img" = ?, "insta_follow" = ?, "insta_follower" = ?, "insta_bio" = ?, "insta_username" = ?, "insta_private" = ?, "insta_verifyed" = ?, "insta_post" = ?, "insta_exturl" = ?, "insta_deepscan" = ? WHERE "insta_id" = ?'

	DB_SELECT_ID_NODE = 'SELECT id FROM "main"."nodes" WHERE ("insta_id") = ?'
	DB_SELECT_USERNAME_NODE = 'SELECT insta_username FROM "main"."nodes" WHERE insta_id = ?'
	DB_SELECT_DONE_NEW_INSTA = 'SELECT done, wait FROM "main"."new_insta" WHERE ("insta_id") = ?'
	DB_SELECT_TARGET_EDGE = 'SELECT target FROM "main"."egdes_insta" WHERE source = ? AND target = ?'
	DB_SELECT_LOGIN_INSTA = 'SELECT * FROM "main"."accounts" WHERE account_type = "instagram"'
	DB_SELECT_LOGIN_PASSWORD_INSTA = 'SELECT password FROM "main"."accounts" WHERE ("username") = ? AND account_type = "instagram"'
	DB_SELECT_OPTIONS = 'SELECT * FROM "main"."options" WHERE what = ?'
	DB_SELECT_ALL_DONE_NEW_INSTA = 'SELECT * FROM "main"."new_insta" WHERE done = 1'
	DB_SELECT_ALL_NODE = "SELECT * FROM main.nodes"
	DB_SELECT_ALL_INSTA_EDGES = "SELECT * FROM main.egdes_insta"
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

	INSTA_MAX_FOLLOW_SCAN_TEXT = "INSTA_MAX_FOLLOW_SCAN"
	INSTA_MAX_FOLLOW_SCAN_VALUE = 2000

	INSTA_MAX_FOLLOW_BY_SCAN_TEXT = "INSTA_MAX_FOLLOW_BY_SCAN"
	INSTA_MAX_FOLLOW_BY_SCAN_VALUE = 2000

	SURFACE_SCAN_TEXT = "SURFACE_SCAN"
	SURFACE_SCAN_VALUE = "0"


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

	Max Follows and Max Followed by
		During search of follows by, where you scan the profile for one user that have completet the singel search you can set a limit to how many followers a user can have or how many it are following. This is to prevent to scan uninterested profils like public organizations and so on as they can have up to 10K. Default is 2000 and is considerated a normal amount of followes/followed by.

	Deepscan and Surfacescan
		By turning on surfacescan you only extract username and instagram id when scraping. This is to save you for request to the server so you can use one user for a longer periode of time, and make the scan go quicker if you are scraping a big nettwork. You can later add specific users found in the graphic to a text file and scan only the ones that are interesting and get all the data.

	ERROR CODES - List of ERROR codes
		001 - INSTAGRAM USER BLOCKED
		002 - TO MANY REQUEST FROM CURRENT USER
		003 - ERROR LOGIN
		004 - USER DONT HAVE ACCESS TO DATA, RETURNING JSON ERROR
		""".format(PROGRAM_NAME, RUN_CURRENT_DISP, RUN_FOLLOW_DISP, RUN_CHANGE_USER, RUN_EXPORT_DATA, DB_DATABASE_EXPORT_FOLDER)

	def __init__(self):
		#Starting up
		print("- Starting {}".format(self.PROGRAM_NAME))
		print("+ Text Libray loaded")
