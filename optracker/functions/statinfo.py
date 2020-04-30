from operator import itemgetter
from tabulate import tabulate

class statInfo():
    def __init__(self, dbTool, dbConn, Zero):
        self.dbTool = dbTool
        self.dbConn = dbConn
        self.zero = Zero

    def getStatforUserNode(self):
        #Load User Able to stat
        statUser = self.getUserStat()

        if statUser != 0:
            #Display it all
            self.zero.printText("\nInsta User: {} ({})".format(statUser[1], statUser[3]), True)
            self.zero.printText("Insta Url: https://instagram.com/{}".format(statUser[8]), True)
            self.zero.printText("Follow from insta: {}".format(statUser[5]), True)
            self.zero.printText("Follower from insta: {}".format(statUser[6]), True)
            self.zero.printText("Private Profil: {}".format(statUser[9]), True)
            self.zero.printText("Posted: {}".format(statUser[11]), True)
            self.zero.printText("\nBio: {}".format(statUser[7]), True)

            #Load Top 10 User Comment
            self.zero.printText("\n--- TOP 10: RECIVED COMMENT ---", True)
            self.getCommentStat(statUser)

            #Load Top 10 User Like
            self.zero.printText("\n--- TOP 10: RECIVED LIKE ---", True)
            self.getLikeStat(statUser)

            #Load Top 10 Post Comment:
            self.zero.printText("\n--- TOP 10: POST WITH COMMENT ---", True)
            self.getTopComment(statUser)

            #Load Top 10 Post Like
            self.zero.printText("\n--- TOP 10: POST WITH LIKES ---", True)
            self.getTopLike(statUser)

            #Likes given
            self.zero.printText("\n--- LIKES GIVEN ---", True)
            self.getLikesByNode(statUser)
            

            #Comments given
            self.zero.printText("\n--- COMMENTS GIVEN ---", True)
            self.getCommentsByNode(statUser)


            #Follow Local

            #Follower Local
        else: self.zero.printError(4)

    def getLikeStat(self, user):
        DATA_LIST = []
        listLike = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_NODE_LIKE_MEDIA, (user[0], ))

        if listLike != 0:
            for x in listLike:
                countLike = int(self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_COUNT_LIKES, (x[0], user[0], ))[0][0])
                DATA_LIST.append((x[0], countLike))

            #Sort Like list
            DATA_LIST.sort(key=itemgetter(1), reverse=True)

            #Table for likes
            TABLE = []
            
            if len(DATA_LIST) <= 10: ra = len(DATA_LIST)
            else: ra = 10

            #Get top 10
            for x in range(ra):
                userName = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ALL_NODE_ID, (DATA_LIST[x][0], ))[0]
                TABLE.append((x+1, userName[1], DATA_LIST[x][1], "https://instagram.com/{}".format(userName[8]), userName[0]))

            print(tabulate(TABLE, headers=["NUMBER", "USER", "LIKES", "URL", "LOCAL ID"], tablefmt='grid'))
        
        else: self.zero.printError(4)

    def getCommentStat(self, user):
        DATA_LIST = []
        listComment = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_NODE_COMMENT_MEDIA, (user[0], ))

        if listComment != 0:
            for x in listComment:
                countComment = int(self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_COUNT_COMMENT, (x[0], user[0], ))[0][0])
                DATA_LIST.append((x[0], countComment))

            #Sort Like list
            DATA_LIST.sort(key=itemgetter(1), reverse=True)

            #Table for likes
            TABLE = []

            if len(DATA_LIST) <= 10: ra = len(DATA_LIST)
            else: ra = 10

            #Get top 10
            for x in range(ra):
                userName = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ALL_NODE_ID, (DATA_LIST[x][0], ))[0]
                TABLE.append((x+1, userName[1], DATA_LIST[x][1], "https://instagram.com/{}".format(userName[8]), userName[0]))

            print(tabulate(TABLE, headers=["NUMBER", "USER", "COMMENTS", "URL", "LOCAL ID"], tablefmt='grid'))
        
        else: self.zero.printError(4)

    def getTopComment(self, user):
        DATA_LIST = []
        listComment = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_MEDIA_COMMENT_MEDIA, (user[0], ))

        if listComment != 0:
            for x in listComment:
                countComment = int(self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_COUNT_MEDIA_COMMENT_MEDIA, (x[0], ))[0][0])
                DATA_LIST.append((x[0], countComment))

            #Sort Like list
            DATA_LIST.sort(key=itemgetter(1), reverse=True)

            #Table for likes
            TABLE = []

            if len(DATA_LIST) <= 10: ra = len(DATA_LIST)
            else: ra = 10

            #Get top 10
            for x in range(ra):
                comDat = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ALL_MEDIA_BASE, (DATA_LIST[x][0], ))[0]
                TABLE.append((x+1, DATA_LIST[x][0], DATA_LIST[x][1], self.zero.insert_newlines(comDat[3]), comDat[10], comDat[6]))

            print(tabulate(TABLE, headers=["NUMBER", "MEDIA_ID", "COMMENTS", "CAPTION", "TYPE", "URL"], tablefmt='grid'))
        
        else: self.zero.printError(4)

    def getTopLike(self, user):
        DATA_LIST = []
        listLike = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_MEDIA_LIKE_MEDIA, (user[0], ))

        if listLike != 0:
            for x in listLike:
                countLike = int(self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_COUNT_MEDIA_LIKES_MEDIA, (x[0], ))[0][0])
                DATA_LIST.append((x[0], countLike))

            #Sort Like list
            DATA_LIST.sort(key=itemgetter(1), reverse=True)

            #Table for likes
            TABLE = []

            if len(DATA_LIST) <= 10: ra = len(DATA_LIST)
            else: ra = 10

            #Get top 10
            for x in range(ra):
                comDat = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ALL_MEDIA_BASE, (DATA_LIST[x][0], ))[0]
                TABLE.append((x+1, DATA_LIST[x][0], DATA_LIST[x][1], self.zero.insert_newlines(comDat[3]), comDat[10], comDat[6]))

            print(tabulate(TABLE, headers=["NUMBER", "MEDIA_ID", "LIKES", "CAPTION", "TYPE", "URL"], tablefmt='grid'))

        else: self.zero.printError(4)

    def getCommentsByNode(self, user):
        DATA_LIST = []
        commentList = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_COMMENT_BY_NODE, (user[0], ))

        if commentList != 0:
            for x in commentList:
                comDat = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_MEDIA_JOIN_NODE, (x[0], ))[0]
                DATA_LIST.append((self.zero.insert_newlines(x[2]), x[0], comDat[16], comDat[15], comDat[10], comDat[6]))

            DATA_LIST.sort(key=itemgetter(3))
            print(tabulate(DATA_LIST, headers=["COMMENT", "MEDIA_ID", "USER", "USER LOCAL ID", "TYPE", "URL"], tablefmt='grid'))
        
        else: self.zero.printError(4)

    def getLikesByNode(self, user):
        DATA_LIST = []
        likeList = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_DISTINCT_LIKEID_NODEID, (user[0], ))

        if likeList != 0:
            for x in likeList:
                count = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_COUNT_LIKE_ID_NODE_ID, (user[0], x[0]))[0][0]
                DATA_LIST.append((count, x[1], x[0], "http://instagram.com/{}".format(x[2])))

            DATA_LIST.sort(key=itemgetter(1))
            print(tabulate(DATA_LIST, headers=["LIKES GIVEN", "USER", "USER LOCAL ID", "URL"], tablefmt='grid'))
        
        else: self.zero.printError(4)


    def getUserStat(self):
        self.zero.printText("\n- Loading somplete users", True)
        userList = self.dbTool.getValueSQLnoinput(self.dbConn, self.zero.DB_SELECT_ALL_SCAN_COMP)

        if userList == 0:
            self.zero.printText("+ No valid users found. \n+They need to have deepscan complete and all post download", True)
            self.zero.printText("\n+ You can enter a local node id, to view the stat avaliable for that user.", True)

            node_id = input(">> Local node id: ")
            user = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ALL_NODE_ID, (node_id, ))[0]
            
            if user == 0:
                self.zero.printText("\n+ Node ID does not exist.", True)
                return 0

            else:
                return user

        else:
            self.zero.printText("+ User list imported", True)
            count = 0
            for i in userList:
                count += 1
                self.zero.printText("[{}] {} ({})".format(count, i[0], str(i[1]).strip()), True)
            
            selectUser = input("+ Select user (1-{}) or [N] for CUSTOM node: ".format(count))

            if not selectUser.isnumeric():
                if selectUser.lower().strip() == "n":
                    node_id = input(">> Local node id: ")
                    user = self.dbTool.getValueSQL(self.dbConn, self.zero.DB_SELECT_ALL_NODE_ID, (node_id, ))[0]
                    
                    if user == 0:
                        self.zero.printText("\n+ Node ID does not exist. #1 selected", True)
                        selectUser = 1

                    else:
                        return user

                else:
                    self.zero.printText("+ Invalid input, #1 selected", True)
                    selectUser = 1

            if int(selectUser) > count:
                self.zero.printText("+ Invalid input, #1 selected", True)
                selectUser = 1

            newNumber = int(selectUser) - 1
            return userList[newNumber]
