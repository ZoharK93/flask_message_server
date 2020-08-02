from pymongo import MongoClient
from cryptography.fernet import Fernet

key = open("secret.key", "rb").read()
enc_password = open("password", "rb").read()

f = Fernet(key)
dec_password = str(f.decrypt(enc_password))[2:-1]
print(dec_password)

client = MongoClient("mongodb+srv://zoharkapustin:%s@flaskserver.qxojc.mongodb.net/messages?retryWrites=true&w=majority" % dec_password)
db = client.messages
collection = db.messages