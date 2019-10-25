<!-- PROJECT LOGO -->
![Imgur](https://i.imgur.com/YpzZFfg.png)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/optracker)
![PyPI](https://img.shields.io/pypi/v/optracker)
![PyPI - Status](https://img.shields.io/pypi/status/optracker)
![PyPI - License](https://img.shields.io/pypi/l/optracker)
![PyPI - Downloads](https://img.shields.io/pypi/dm/optracker)
![Discord](https://img.shields.io/discord/633751704868749322)


# openSource Tracker
Easy to use program for scraping openSources, saves data and enable you to analyze it in your favorite graphic display. I created the projected based on <a href="https://github.com/realsirjoe/instagram-scraper">instagram scraper</a>, witch allows you to get data from Instagram without API. The goal of this project is to make it easy for everyone to gather openSource content and analyze it.


<!-- CONTENT -->
## How to install
***Simply run:***
```cmd
pip install optracker
```

***Or download the project via git clone and run the following:***
```cmd
pip install -r requirements.txt
python .\run_tracker.py
```

## Getting Started
The projects found here are for my own study for confirming and testing out theory according to social network analyzing. They can be used and altered as you see fit. To use it you need to install some required library for python see install.

### 1. Running the program
To run simply type: **optracker** in console if you installed it from PIP. If you downloaded it from github: **python .\run_tracker.py** from the optracker directory.<br />
<br />
***NB! You will need to run the script as administrator if you are using windows***

### 2. Userlist
The program need functional accounts to work. They can either be added manually when you run it for the first time. Or create a local file with usernames and password. They will then be added to the database automatically on startup. In experience you need more then one user account to scan large list of users so your user don't get blocked because of to many requests.

>**The following user list can be created:**
>- inst_user.txt
>- face_user.txt
>- user_list.txt

You don't need to have a separate list for facebook or instagram but some people prefer it. You can add all the userdata in the same file by using user_list.txt. They all need to be setup the same way anyway.

```python
#Setup for user_list file
{USERNAME}, {PASSWORD}, {EMAIL}, {FULLNAME}, {ACCOUNT}
```
Account type can be: **facebook** or **instagram**. It is so the program know witch account to use where.

```python
#Example of insta_user.txt
my_username, my_password, my_email, my_fullname, instagram
my_username2, my_password2, my_email3, my_fullname2, facebook
my_username3, my_password3, my_email3, my_fullname3, instagram
```

**User list** will update each time you start the program, so new users can be added directly into the .txt document or you can add them manually into the program at start up.

**Place for userlist** are in root directory. Usually is it ***c:\optracker*** or ***\optracker*** for Linux
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
When you run the program it will first try to connect to Instagram, if youdon'tt have a user file you will be asked to enter a username and password. After that you will get the option to choose from a menu. Start by running a single scan of one account. After that you can run more single scan to grow your node database or use follow by scan options. You also have a help menu that will give you all the information you need.<br />

> ### Root Folder
> Root folder for the program are the lowest dir. Usally is it ***c:\optracker*** or ***\optracker*** for linux

### 4. First time scraping
The first time you scrape all the users will be saved as nodes. This will take some time, since we also want to save all the info we can get for each node. During this a lot of request will be send to the target server for the scrape, and as a result some of your user account may be blocked because of to many request in a short time. Laster when you scrape instagram as an example it will check if the node all ready exist in your database, if so it only add the connections it finds and your request to the server fall. Conclusion is that the bigger node base you have the faster you can scrape, and less request will be made.

###	5. Scan all follower
You will be presented with a list of users that you have finnished adding to your database. The program will then scan all the connections it has that are not private, add the nodes to DB and connections in edges.

### 6. Max Follows and Max Followed by
During **Scan all follower**, where you scan the profile for one user that have completet the singel search you can set a limit to how many followers a user can have or how many it are following. This is to prevent to scan uninterested profils like public organizations and so on as they can have up to 10K. Default is 2000 and is considerated a normal amount of followes/followed by.

### 7. Deepscan and Surfacescan
By turning on surfacescan you only extract username and instagram id when scraping. This is to save you for request to the server so you can use one user for a longer periode of time, and make the scan go quicker if you are scraping a big nettwork. You can later add specific users found in the graphic to a text file and scan only the ones that are interesting and get all the data.

### 8. Deepscan from list
Gives you the possibility to run a deep scan on a selected list of users. It will scrape all the data from instagram for the selected ones, and update DB Node. You need to create a file in **ROOT FOLDER** called **user_scan_insta.txt**
```
optracker/
  userlist.txt
  user_scan_insta.txt
  db/
    openSource-tracker.db
  export/
    node.csv
    egdes.csv
```
Content of the list need to be one username per line:
```python
{USER 1}
{USER 2}
{USER 3}
{USER 4}
```
### 9. Detail Print
On Default is it turned **OFF** you will only get the minimum of info to see if it is working properly. If you turn it **ON** will you be presented with all the output the scraper have. 

### 10. Change default value
From the menu can you change default values like surfacescan, max follow and mysql or sqlite with more. To change select yes, fill in new value, if you dont want to change one value leave it blank.


## Database Information
By default the scraper use **SQLite**, all the data are stored in **optracker/db/openSource-tracker.db**. 

> **MySQL** are also available to use. Current version tested and found OK is **MySQL 8.0.18**. You can change the database settings in the menu. But you need to download and install the latest version of Mysql and create a database called **openSource-tracker**, if you dont have an online version you want to use instead of local. Also remember to use **utf8mb4**. The following are default:
> * DB_MYSQL = "localhost"
> * DB_MYSQL_USER = "optracker"
> * DB_MYSQL_PASSWORD = "localpassword"
> * DB_MYSQL_DATABASE = "openSource_tracker"
> * DB_MYSQL_PORT = "3306"
> * DB_MYSQL_ON = 0
> * DB_MYSQL_COLLATION = "utf8mb4_general_ci"
> * DB_MYSQL_CHARSET = "utf8mb4"  
>   
>***Scraping big amount of data can be really slow if you use SQLite, therefore are MySQL an option if you plan on collectingg huge amounts.*** 

**The database consist of the following tabels:**
- accounts
- edges_insta
- nodes
- options
- new_insta

> **Note!** All SQL data are saved in **optracker.config** located in root folder. The format are in JSON and you can change it as you would like to match your current DB. But I recomend to keep the standar settings. 


### 1. Accounts
Stores all your usernames and password for the different openSource sites.

### 2. Edges_insta
Have list of all the connections. Rows are target, source, weight and type. This is all made to be used with gephi for visualizing the data in graph form. The numbers are connected to ID in nodes. Show how is following or connected to who.

### 3. nodes
List of all the nodes created. They all have their own ID. It also contain all information scraped on a single user like username, email, bio and so on found in the different scraping sites.

### 4. Options
Temporary table to store information like follow list, last search and so on for the program to use.

### 5. New_insta
This table have a list of all instagram accounts that have been found during scraping. The program will used this to see witch account have not yet been fully scraped. When it is finnish are the account set to DONE. If you dont want the account to be scraped set the WAIT value to True. 0 = False, 1 = True. ***This can also be used in the case of a user have to many follower, or non at all so you dont want to scan it. When the user pop up, the scanner jumps over it.***

### 6. Export
To export the data you can connect to the DB file under the db/folder. Or you can export it from the program. From main menu choose export. It will the generate two files **nodes.csv** and **egdes.csv**. You can then import this into your favorite graphic display

## Common Error
### 1. F String
```python
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
To fix update python to latest, you are using an old version that dosent support **f""** you need to use **python3.6**

### 2. Instagram useragent
```
ERROR: {"message": "useragent mismatch", "status": "fail"}
```
Igramscraper are using a useragent that are not up to date. You need to update **self.user_agent** in **igramscraper/instagram.py**. Locate this file and look for somethong that looks like this:
```python
self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) ' \
                          'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/66.0.3359.139 Safari/537.36'
```
After this change it to a new useragent that are allowed by instagram, this is one example that worked in october 2019.
```python
self.user_agent =   'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X)' \
                            'AppleWebKit/605.1.15 (KHTML, like Gecko)' \
                            'Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
```

### 3. Private Instagram
```python
  File "\optracker\functions\instagram_func.py", line 20, in get_insta_following
    following = self.instagram.get_following(insta_id, totalFollow, self.page_size_check(totalFollow), delayed=True)
  File "\optracker\igramscraper\instagram.py", line 963, in get_following
    Instagram.HTTP_FORBIDDEN)
optracker.igramscraper.exception.instagram_exception.InstagramException: Failed to get follows of account id ******. The account is private., Code:403
```
When searhing profiles sometimes the user have set it to private after first scraping. When extracting data after this the program will stop and give an error that the profile is private. Just run it once more, the program have updated the profile automatic to private so it wont happen on the next scan. 

## Common Information

- Look at TODO if you want to help: [TODO](https://github.com/suxSx/opensource-tracker/blob/master/TODO.md) <br />
- Read the CODE of Conduct before you edit: [Code of Conduct](https://github.com/suxSx/opensource-tracker/blob/master/CODE_OF_CONDUCT.md)<br />
- We use MIT License: [MIT](https://github.com/suxSx/opensource-tracker/blob/master/LICENSE.md)

### Worth mentioning
- instagram-php-scraper [here](https://github.com/postaddictme/instagram-php-scraper/)<br />
- instagram-scraper [here](https://github.com/realsirjoe/instagram-scraper)<br />
- logo-design [here](http://freepik.com)  
