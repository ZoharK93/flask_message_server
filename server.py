from flask import Flask, request
from db_connection import get_collection
from functions import *
import os
import sys

app = Flask(__name__)

def run_function(request,callback):
    try:
        collection = get_collection()
        return callback(request,collection)
    except:
        e = sys.exc_info()
        return 'An error has occured: %s' % str(e)

@app.route('/', methods=['GET'])
def home():
    #Route for getting messages intended for a specific user (all/read/unread)
    return run_function(request,read_messages)
    

@app.route('/write', methods=['POST'])
def write():
    #Route for writing messages
    return run_function(request,write_message)

@app.route('/read', methods=['GET'])
def read():
    #Route for reading one message    
    return run_function(request,read_one)

@app.route('/delete', methods=['DELETE'])
def delete():
    #Route for deleting one message
    return run_function(request,delete_message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)