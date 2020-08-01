from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from bson.json_util import dumps
import json

app = Flask(__name__)

client = MongoClient("mongodb+srv://zoharkapustin:9arboGgKkr5WGxV3@flaskserver.qxojc.mongodb.net/messages?retryWrites=true&w=majority")
db = client.messages
collection = db['messages']

def parse_message_with_id(message):
    parsed_message = {k:v for k,v in message.items() if k != '_id'}
    parsed_message['_id'] = str(message['_id'])
    return parsed_message

@app.route('/', methods=['GET'])
def home():
    user = request.args.get('user')
    cond = request.args.get('read')
    query = {'receiver' : user}
    if cond != None: query['read'] = cond == 'true'
    messages = collection.find(query)
    parsed_messages = []
    for message in messages: 
        parsed_messages.append(parse_message_with_id(message))
    return {'messages' : parsed_messages}

@app.route('/write', methods=['POST'])
def write():
    data = dict(request.form).copy()
    data['creation date'] = str(datetime.date(datetime.now()))
    data['read'] = False
    res = collection.insert_one(data)
    return str(res.inserted_id)

@app.route('/read', methods=['GET'])
def read():
    message_id = request.args.get('id')
    res = collection.find_one_and_update({'_id' : ObjectId(message_id)}, {'$set' : {'read' : True}})
    return parse_message_with_id(res)

@app.route('/delete', methods=['DELETE'])
def delete():
    message_id = request.args.get('id')
    res = collection.delete_one({'_id' : ObjectId(message_id)})
    return str(res.raw_result)

if __name__ == '__main__':
    app.run()