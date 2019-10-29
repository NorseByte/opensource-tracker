<p align="center"><img src="https://i.imgur.com/i1FMPUZ.png" alt="drawing" width="300" /></p>

# Todo:
- [x] 27-10-2019 (U) Add update Node data when you run a check of node DB.
- [ ] Make the code smaller. Repeating steps can be shorten
- [x] 27-10-2019 (U) Make a stop function for if profile is private
- [ ] Add try and catch in get user info. To enable error handling.
- [ ] Make database for followers, and follower for easy rollback on error (delete when current user are done, and keypoint for insta user.)
- [ ] Add functions scan keywords. (Look for specific keywords in user profiles (node) and then use a full single scan)
- [ ] Add other platforms for data gathering
- [x] 18-10-2019 (U) Added surface/deep scan.
- [x] 01-10-2019 (U) Check up on Finnish status message in DB_TABLE_NEW_INSTA
- [x] 07-10-2019 (U) Add max follower criteria in search options.
- [x] 11-10-2019 (U) Root directory, PIP install, class updates.
- [ ] Add user creation options
- [x] 18-10-2019 (U) User DB NODE are updated in setCurrentUser(). And in userselect when scanFollowBy().
- [x] 27-10-2019 (U) Scan user from DB og text that have Deep = 0
- [x] 18-10-2019 (U) Added scan options for users in txt document.
- [x] 19-10-2019 (P) updateNodesUser() ERROR fix.
- [x] 28-10-2019 (U) Detail print added show minimum text or all.
- [ ] Add node-type to node, is it person, page with more.

## Rules
When something are done, mark it as finnish and add date of completions and what kind of edit was made.
- (U) = UPDATE
- (P) = PATCH
- (N) = NEW

Exampel:
- `07-10-2019 (P) Fix bug on line 127 in core.py`
- `07-10-2019 (U) Added better search options`
- `07-10-2019 (N) New functions added able to export into xml`
