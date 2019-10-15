<p align="center">
<img src="https://i.imgur.com/jHHevZ2.png">
<h1 align="center">openSource Tracker</h1>
  <p align="center">Project used during my study of openSource gathering. I created the projected based on <a href="https://github.com/realsirjoe/instagram-scraper">instagram scraper</a>, witch allows you to get data from Instagram without API.
  </p>
</p>

## How to install
***Simply run:***
```
pip install optracker
```

***Or download the project via git clone and run the following:***
```
pip install -r requirements.txt
python .\run_tracker.py
```

## Getting Started
The projects found here are for my own study for confirming and testing out theorys according to social nettwork analysing. They can be used and altered as you see fit. To use it you need to install some requiered libray for python see install.

### 1. Running the program
To run simply type: **optracker** in console if you installed it from PIP. If you downloaded it from github: **python .\run_tracker.py** from the optracker directory.<br />
<br />
***NB! You will need to run the script as administrator if you are using windows***

### 2. Userlist
The program need functional accounts to work. They can either be added manually when you run it for the first time. Or create a local file with usernames and password. They will then be added to the database automatical on startup. In experience you need more then one user account to scan large list of users so your user dont get blocked becouse of to many requests.

**The following user list can be created:**
- inst_user.txt
- face_user.txt
- user_list.txt

You dont need to have a seperate list for facebook or instagram but some people prefere it. You can add all the userdata in the same file by using user_list.txt. They all need to be setup the excate same way anyway.

```
#Setup for user_list file
{USERNAME}, {PASSWORD}, {EMAIL}, {FULLNAME}, {ACCOUNT}
```
Account type can be: **facebook** or **instagram**. It is so the program know witch account to use where.

```
#Example of insta_user.txt
my_username, my_password, my_email, my_fullname, instagram
my_username2, my_password2, my_email3, my_fullname2, facebook
my_username3, my_password3, my_email3, my_fullname3, instagram
```

**User list** will update each time you start the program, so new users can be added directly into the .txt document or you can add them manually into the program at start up.

**Place for userlist** are in root directory. Usally is it ***c:\optracker*** or ***\optracker*** for linux
```
optracker/
  userlist.txt
  db/
    openSource-tracker.db
  export/
    node.csv
    egdes.csv
```


### 3. How to use
When you run the program it will first try to connect to Instagram, if you dont have a user file you will be asked to enter a username and password. After that you will get the option to choose from a menu. Start by running a singel scan of one account. After that you can run more singel scan to grow your node database or use follow by scan options. You also have a help menu that will give you all the information you need.<br />
<br />
Root folder for the program are the lowest dir. Usally is it ***c:\optracker*** or ***\optracker*** for linux

### 4. First time scraping
The first time you scrape all the users will be saved as nodes. This will take some time, since we also want to save all the info we can get for each node. During this a lot of request will be send to the target server for the scrape, and as a result some of your user account may be blocked because of to many request in a short time. Laster when you scrape instagram as an example it will check if the node all ready exist in your database, if so it only add the connections it finds and your request to the server fall. Conclusion is that the bigger node base you have the faster you can scrape, and less request will be made.

## Database Information
All the data are stored in **optracker/db/openSource-tracker.db**

**The database consist of the following tabels:**
- accounts
- edges_insta
- nodes
- options
- new_insta

### 1. Accounts
Stores all your usernames and password for the different openSource sites.

### 2. Edges_insta
Have list of all the connections. Rows are target, source, weight and type. This is all made to be used with gephi for visualising the data in graph form. The numbers are connected to ID in nodes. Show how is following or connected to who.

### 3. nodes
List of all the nodes created. They all have their own ID. It also contain all information scraped on a single user like username, email, bio and so on found in the dirrent scraping sites.

### 4. Options
Tempory table to store information like follow list, last search and so on for the program to use.

### 5. New_insta
This table have a list of all instagram accounts that have been found during scraping. The program will used this to see witch account have not yet been fully scraped. When it is finnish are the account set to DONE. If you dont want the account to be scraped set the WAIT value to True. 0 = False, 1 = True.

### 6. Export
To export the data you can connect to the DB file under the db/folder. Or you can export it from the program. From main menu choose export. It will the generate two files **nodes.csv** and **egdes.csv**. You can then import this into your favourite graphic displayer.


## Todo:
```
- Add update Node data when you run a check agenst node DB.
- Add autoupdate for new information in db
- Make the code smaller. Repiting steps can be shorten
- Make a stop function for if profile is private
- Add try and catch in get user info. To enable error handeling.
- Make database for followers, and follower for easy rolback on error
  (delete when current user are done, and keypoint for insta user.)
- Add functions scan keywords.
  (Look for specfic keywords in user profiles (node) and then use a full singel scan)
```

## Updates:
```
- 01-10-2019 (U) Check up on finnish status message in DB_TABLE_NEW_INSTA
- 07-10-2019 (U) Add max follower critera in search options.
- 11-10-2019 (U) Root directory, PIP install, class updates.

(U) = UPDATE, (P) = PATCH, (N) = NEW
```

## Common Error

### 1. F String
```
Traceback (most recent call last):
  File "/usr/local/bin/optracker", line 6, in <module>
    from optracker.optracker import run
  File "/usr/local/lib/python3.5/dist-packages/optracker/optracker.py", line 14, in <module>
    from igramscraper.instagram import Instagram
  File "/usr/local/lib/python3.5/dist-packages/igramscraper/instagram.py", line 153
    cookies += f"{key}={session[key]}; "
                                       ^
SyntaxError: invalid syntax
```
To fix update python to latest, you are using an old version that dosent support **f""**.

### 2. Instagram useragent
```
ERROR: {"message": "useragent mismatch", "status": "fail"}
```
Igramscraper are using a useragent that are not up to date. You need to update **self.user_agent** in **igramscraper/instagram.py**. Locate this file and look for somethong that looks like this:
```
self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) ' \
                          'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/66.0.3359.139 Safari/537.36'
```
After this change it to a new useragent that are allowed by instagram, this is one example that worked in october 2019.
```
self.user_agent =   'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X)' \
                            'AppleWebKit/605.1.15 (KHTML, like Gecko)' \
                            'Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
```

## Other
instagram-php-scraper [here](https://github.com/postaddictme/instagram-php-scraper/)<br />
instagram-scraper [here](https://github.com/realsirjoe/instagram-scraper)<br />
logo-design-ide [here] (http://www.freepik.com)
