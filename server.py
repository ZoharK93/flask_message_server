from flask import Flask, request
from datetime import datetime
from bson.objectid import ObjectId
from db_connection import collection
import os

app = Flask(__name__)

def build_query(request,mode):
    user = request.headers.get('user')
    message_id = request.args.get('id')
    query = {'$or' : [{'sender' : user}, {'receiver' : user}]} if mode == 'delete' else {'receiver' : user}
    if message_id != None:
        query = {'$and' : [{'_id' : ObjectId(message_id)}, query]}
    return query

@app.route('/', methods=['GET'])
def home():
    user = request.headers.get('user')
    cond = request.args.get('read')
    query = {'receiver' : user}
    if cond != None: query['read'] = cond == 'true'
    messages = collection.find(query)
    parsed_messages = []
    for message in messages:
        parsed_message = {k:v for k,v in message.items() if k != '_id'}
        parsed_message['_id'] = str(message['_id']) 
        parsed_messages.append(parsed_message)
    return {'messages' : parsed_messages}

@app.route('/write', methods=['POST'])
def write():
    data = dict(request.form).copy()
    data['creation date'] = str(datetime.date(datetime.now()))
    data['read'] = False
    data['sender'] = request.headers.get('user')
    res = collection.insert_one(data)
    return str(res.inserted_id)

@app.route('/read', methods=['GET'])
def read():
    res = collection.find_one_and_update(build_query(request,'read'), {'$set' : {'read' : True}})
    return str(res)

@app.route('/delete', methods=['DELETE'])
def delete():
    res = collection.find_one_and_delete(build_query(request,'delete'))
    return str(res)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)