import pymysql
import requests
import uuid
import time
import datetime
import bleach
import json

class HighLow:

    def __init__(self, host, username, password, database, high_low_id=None):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.high_low_id = bleach.clean(high_low_id)
        self.high = ""
        self.low = ""
        self.timestamp = None
        self.protected_columns = []

    def create(self, uid, high, low):
        ## Create a new High/Low entry in the database ##
        #Connect to MySQL
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Create a High/Low ID
        self.high_low_id = str( uuid.uuid1() )

        #Clean the High and Low data
        self.high = bleach.clean(high)
        self.low = bleach.clean(low)

        #Now, insert the data
        cursor.execute("INSERT INTO highlows(highlowid, uid, high, low, total_likes) VALUES('" + self.high_low_id + "', '" + uid + "', '" + self.high + "', '" + self.low + "', 0);")

        #Commit and close the connection
        conn.commit()
        conn.close()
        
        #Return the HighLow ID
        return '{ "highlowid":"' + self.high_low_id + '" }'



    def update(self, high, low):
        ## Update the High/Low database entry ##
        #Connect to MySQL
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Now, get and clean the High and Low
        self.high = bleach.clean(high)
        self.low = bleach.clean(low)

        #Update the data
        cursor.execute("UPDATE highlows SET high='" + self.high + "', low='" + self.low + "' WHERE highlowid='" + self.high_low_id + "';")

        #Commit and close the connection
        conn.commit()
        conn.close()



    def delete(self):
        ## Delete the HighLow database entry ##
        #Connect to MySQL
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Delete the entry
        cursor.execute("DELETE FROM highlows WHERE highlowid='" + self.high_low_id + "';")

        #Commit and close the connection
        conn.commit()
        conn.close()

    
    def update_total_likes(self):
        ## Count the number of likes in the database that belong to the current high/low ##
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        cursor.execute( "SELECT id FROM likes WHERE highlowid='{}'".format(self.high_low_id) )

        likes = cursor.fetchall()
        total_likes = len(likes)

        cursor.execute( "UPDATE highlows SET total_likes={} WHERE highlowid='{}'".format(total_likes, self.high_low_id) )

        conn.commit()
        conn.close()

    def like(self, uid):
        ## Add a new entry to the "Likes" table 
        #Connect to MySQL
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Create the entry
        cursor.execute( "INSERT INTO likes(highlowid, uid) VALUES('{}', '{}');".format(self.high_low_id, uid) )

        #Commit and close the connection
        conn.commit()
        conn.close()

    def unlike(self, uid):
        ## Remove the entry in the "Likes" table that corresponds to the current user and this high/low ##
        #Connect to MySQL
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Delete the entry, if it exists
        cursor.execute( "DELETE FROM likes WHERE highlowid='{}' AND uid='{}';".format(self.high_low_id, uid) )

        #Commit and close the connection
        conn.commit()
        conn.close()

    
    def comment(self, uid, message):
        #Collect the specified data and add to the database
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        commentid = str( uuid.uuid1() )

        #Clean the message
        cleaned_message = bleach.clean(message)

        cursor.execute( "INSERT INTO comments(commentid, highlowid, uid, message) VALUES('{}', '{}', '{}', '{}');".format(commentid, self.high_low_id, uid, cleaned_message) )

        conn.commit()
        conn.close()

    def update_comment(self, uid, commentid, message):
        #Find the comment and udpate the database
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #TODO: Should we update the timestamp or not?

        cleaned_message = bleach.clean(message)
        cleaned_commentid = bleach.clean(commentid)
        
        cursor.execute( "UPDATE comments SET message='{}' WHERE commentid='{}' AND highlowid='{}' AND uid='{}';".format(cleaned_message, cleaned_commentid, self.high_low_id, uid) )

        conn.commit()
        conn.close()

    def delete_comment(self, uid, commentid):
        #Find the comment and udpate the database
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        cleaned_commentid = bleach.clean(commentid)

        cursor.execute( "DELETE FROM comments WHERE commentid='{}' AND uid='{}' AND highlowid='{}';".format(cleaned_commentid, uid, self.high_low_id) )

        conn.commit()
        conn.close()

    def get(self, uid, column_name):

        column_name = bleach.clean(column_name)

        if column_name in self.protected_columns:
            return '{ "error": "column_unavailable" }'

        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        cursor.execute( "SELECT {} FROM highlows WHERE highlowid='{}';".format(column_name, self.high_low_id) )

        result = cursor.fetchone()

        return json.dumps( { "result": result[column_name] } )