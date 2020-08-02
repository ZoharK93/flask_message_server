from pymongo import MongoClient

client = MongoClient("mongodb+srv://zoharkapustin:9arboGgKkr5WGxV3@flaskserver.qxojc.mongodb.net/messages?retryWrites=true&w=majority")
db = client.messages
collection = db.messages