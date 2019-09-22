# openSource Tracker
Files used during my study of openSource gathering at Krigsskolen. I created the projected based on [instagram scraper](https://github.com/realsirjoe/instagram-scraper), witch allows you to get data from Instagram without API.

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

### 3. First time scraping
The first time you scrape all the users will be saved as nodes. This will take some time, since we also want to save all the info we can get for each node. During this a lot of request will be send to the target server for the scrape, and as a result some of your user account may be blocked because of to many request in a short time. Laster when you scrape instagram as an example it will check if the node all ready exist in your database, if so it only add the connections it finds and your request to the server fall. Conclusion is that the bigger node base you have the faster you can scrape, and less request will be made.  

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
```

## Other
instagram-php-scraper [here](https://github.com/postaddictme/instagram-php-scraper/)<br />
instagram-scraper [here](https://github.com/realsirjoe/instagram-scraper)
