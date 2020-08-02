from pymongo import MongoClient
from cryptography.fernet import Fernet

key = b'nU4OsrvjYBQA28NG5CvCphW87Cr3y9VEvyNoqF3x_mA='
enc_password = open("password", "rb").read()

f = Fernet(key)
dec_password = str(f.decrypt(enc_password))[2:-1]

client = MongoClient("mongodb+srv://zoharkapustin:%s@flaskserver.qxojc.mongodb.net/messages?retryWrites=true&w=majority" % dec_password)
db = client.messages
collection = db.messages