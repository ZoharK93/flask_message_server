from pymongo import MongoClient
from cryptography.fernet import Fernet
import sys

#Decrypt the encrypted password stored in the file 'password'
key = b'nU4OsrvjYBQA28NG5CvCphW87Cr3y9VEvyNoqF3x_mA='
enc_password = open("password", "rb").read()
f = Fernet(key)
dec_password = str(f.decrypt(enc_password))[2:-1]

def get_collection():
    #Establishes a connection to the database, and returns the 'messages' collection
    try:
        client = MongoClient("mongodb+srv://zoharkapustin:%s@flaskserver.qxojc.mongodb.net/messages?retryWrites=true&w=majority" % dec_password)
        db = client.messages
        return db.messages
    except:
        e = sys.exc_info()
        return 'There was an error connecting to the database: %s' % str(e)