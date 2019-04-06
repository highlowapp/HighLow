import pymysql
import requests
import uuid
import time
import datetime
import bleach

class HighLow:

    def __init__(self, host, username, password, database, high_low_id=None):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.high_low_id = high_low_id
        self.high = ""
        self.low = ""
        self.timestamp = None

    def create(self, token, high, low):

        ## Create a new High/Low entry in the database ##
        #Verify the user

        #Make a request to the auth service
        authentication_request = requests.post("http://auth_service/verify_token", headers={'Authorization':'Bearer ' + str(token) })

        #Parse the response as JSON
        authentication_request_json = authentication_request.json()


        #If there was an error, return an error
        if "error" in authentication_request_json:
            return '{ "error":"' + authentication_request_json["error"] + '" }'

        #Get the UID
        uid = authentication_request_json["uid"]

        #Connect to MySQL
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Create a High/Low ID
        self.high_low_id = str( uuid.uuid1() )

        #Get the timestamp
        timestamp = time.mktime( datetime.datetime.now().timetuple() )

        #Clean the High and Low data
        self.high = bleach.clean(high)
        self.low = bleach.clean(low)

        #Now, insert the data
        cursor.execute("INSERT INTO highlows(highlowid, uid, high, low, total_likes, timestamp) VALUES('" + self.high_low_id + "', '" + uid + "', '" + self.high + "', '" + self.low + "', 0, " + timestamp + ";")

        #Commit and close the connection
        conn.commit()
        conn.close()
        
        #Return the HighLow ID
        return '{ "highlowid":"' + self.high_low_id + '" }'



    def update(self, token, high, low):
        ## Update the High/Low database entry ##
        #Verify the user

        #Make a request to the auth service
        authentication_request = requests.post("http://auth_service/verify_token", headers={'Authorization':'Bearer ' + str(token) })

        #Parse the response as JSON
        authentication_request_json = authentication_request.json()


        #If there was an error, return an error
        if "error" in authentication_request_json:
            return '{ "error":"' + authentication_request_json["error"] + '" }'

        #Get the UID
        uid = authentication_request_json["uid"]

        #Connect to MySQL
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Now, get and clean the High and Low
        self.high = bleach.clean(high)
        self.low = bleach.clean(low)

        #Update the data
        cursor.execute("UPDATE highlows SET high='" + self.high + "', low='" + self.low + "' WHERE highlowid='" + self.high_low_id + "' AND uid='" + uid + "';")

        #Commit and close the connection
        conn.commit()
        conn.close()



    def delete(self, token):
        ## Delete the HighLow database entry ##
        #Verify the user

        #Make a request to the auth service
        authentication_request = requests.post("http://auth_service/verify_token", headers={'Authorization':'Bearer ' + str(token) })

        #Parse the response as JSON
        authentication_request_json = authentication_request.json()


        #If there was an error, return an error
        if "error" in authentication_request_json:
            return '{ "error":"' + authentication_request_json["error"] + '" }'

        #Get the UID
        uid = authentication_request_json["uid"]

        #Connect to MySQL
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Delete the entry
        cursor.execute("DELETE FROM highlows WHERE highlowid='" + self.high_low_id + "' AND uid='" + uid + "';")

        #Commit and close the connection
        conn.commit()
        conn.close()

    
    #TODO: Add functions for getting data, liking, and commenting
     
