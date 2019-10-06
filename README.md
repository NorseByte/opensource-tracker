# openSource Tracker
Files used during my study of openSource gathering. I created the projected based on [instagram scraper](https://github.com/realsirjoe/instagram-scraper), witch allows you to get data from Instagram without API.

## How to install
***Simply run:***
```
pip install optracker
```

***Or download the project via git clone and run the following:***
```
pip install -r requirements.txt
```

## Getting Started
The projects found here are for my own study for confirming and testing out theorys according to social nettwork analysing. They can be used and altered as you see fit. To use it you need to install some requiered libray for python see install.

### 1. Running the program
To run simply type: **python .\optracker.py** from the optracker directory.<br />
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
username, password, email, fullname, {ACCOUNT}
```
Account type can be: **facebook** or **instagram**. It is so the program know witch account to use where.

```
#Example of insta_user.txt
my_username, my_password, my_email, my_fullname, instagram
my_username2, my_password2, my_email3, my_fullname2, facebook
my_username3, my_password3, my_email3, my_fullname3, instagram
```

**User list** will update each time you start the program, so new users can be added directly into the .txt document or you can add them manually into the program at start up.

### 3. How to use
When you run the program it will first try to connect to Instagram, if you dont have a user file you will be asked to enter a username and password. After that you will get the option to choose from a menu. Start by running a singel scan of one account. After that you can run more singel scan to grow your node database or use follow by scan options. You also have a help menu that will give you all the information you need.

### 4. First time scraping
The first time you scrape all the users will be saved as nodes. This will take some time, since we also want to save all the info we can get for each node. During this a lot of request will be send to the target server for the scrape, and as a result some of your user account may be blocked because of to many request in a short time. Laster when you scrape instagram as an example it will check if the node all ready exist in your database, if so it only add the connections it finds and your request to the server fall. Conclusion is that the bigger node base you have the faster you can scrape, and less request will be made.

## Database Information
All the data are stored in **db/**

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


## Todo:
```
- Add update Node data when you run a check agenst node DB.
- Add autoupdate for new information in db
- Check up on finnish status message in DB_TABLE_NEW_INSTA
- Make the code smaller. Repiting steps can be shorten
- Make automation on search for new_insta
- Make a stop function for if profile is private
- Add try and catch in get user info. To enable error handeling.
- Make database for followers, and follower for easy rolback on error
  (delete when current user are done, and keypoint for insta user.)
- Add functions scan keywords.
  (Look for specfic keywords in user profiles (node) and then use a full singel scan)
- Add max follower critera in search options.
```

## Other
instagram-php-scraper [here](https://github.com/postaddictme/instagram-php-scraper/)<br />
instagram-scraper [here](https://github.com/realsirjoe/instagram-scraper)
