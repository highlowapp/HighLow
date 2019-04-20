import pymysql
import requests
import time 
import datetime
import bleach
import json



class HighLowList:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def get_highlows_for_user(self, uid, sortby=None, limit=None):
        #Connect to MySQL
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        uid = bleach.clean(uid)

        cursor.execute("SELECT * FROM highlows WHERE uid='{}' ORDER BY _timestamp DESC;".format(uid))

        highlows = cursor.fetchall()

        if sortby != None:

            options = {

                "latest": (None, False), 
                "oldest": (None, True),
                "most_likes": ("total_likes", True)

            }

            if options[sortby][0] == None:
                highlows = sorted(highlows, reverse=options[sortby][1])
            else:
                highlows = sorted(highlows, key=lambda a: a[ options[sortby][0] ], reverse=options[sortby][1])

        if limit != None:
            if limit <= len(highlows) - 1:
                highlows = highlows[0:limit+1]

        return highlows

