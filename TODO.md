<img src="https://i.imgur.com/i1FMPUZ.png" alt="drawing" width="300" align="middle"/>

# Todo:
- [ ] Add update Node data when you run a check of node DB.
- [ ] Add auto update for new information in db
- [ ] Make the code smaller. Repeating steps can be shorten
- [ ] Make a stop function for if profile is private
- [ ] Add try and catch in get user info. To enable error handling.
- [ ] Make database for followers, and follower for easy rollback on error (delete when current user are done, and keypoint for insta user.)
- [ ] Add functions scan keywords. (Look for specific keywords in user profiles (node) and then use a full single scan)
- [ ] Add other platforms for data gathering
- [ ] Create deep and surface scan (scan only username, scan full profile)
- [x] 01-10-2019 (U) Check up on Finnish status message in DB_TABLE_NEW_INSTA
- [x] 07-10-2019 (U) Add max follower criteria in search options.
- [x] 11-10-2019 (U) Root directory, PIP install, class updates.
- [ ] Add user creation options
- [ ] Add get info for user after surface scan

## Rules 
When something are done, mark it as finnish and add date of completions and what kind of edit was made.
- (U) = UPDATE 
- (P) = PATCH
- (N) = NEW

Exampel: 
- `07-10-2019 (P) Fix bug on line 127 in core.py`
- `07-10-2019 (U) Added better search options`
- `07-10-2019 (N) New functions added able to export into xml`
