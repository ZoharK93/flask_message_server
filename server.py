from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
import json

app = Flask(__name__)

client = MongoClient("mongodb+srv://zoharkapustin:9arboGgKkr5WGxV3@flaskserver.qxojc.mongodb.net/messages?retryWrites=true&w=majority")
db = client.messages
collection = db['unread_messages']

@app.route('/', methods=['GET'])
def home():
    return collection.find_one()['message']

@app.route('/write', methods=['POST'])
def write():
    data = dict(request.form).copy()
    data['creation date'] = str(datetime.date(datetime.now()))
    print(data)
    collection.insert_one(data)
    return "ok"

if __name__ == '__main__':
    app.run()