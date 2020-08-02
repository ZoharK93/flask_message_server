from datetime import datetime
from bson.objectid import ObjectId

def build_query(request,mode):
    '''
    A function that builds a MongoDB query for delete/read one message.
    
    Parameters:
        request - the HTTP request that initiated the transaction.
        mode - either 'delete' or 'read'.
    '''
    user = request.headers.get('user')
    message_id = request.args.get('id')
    query = {'$or' : [{'sender' : user}, {'receiver' : user}]} if mode == 'delete' else {'receiver' : user}
    if message_id != None:
        query = {'$and' : [{'_id' : ObjectId(message_id)}, query]}
    return query


def read_messages(request,collection):
    '''
    Returns messages for a specific user - specified in the request headers.
    If no user was specified, returns an empty array.

    Optional request argument:
        read - true/false, returns read/unread messages respectively. 
            If this parameter is not present, returns all messages.
    '''
    user = request.headers.get('user')
    cond = request.args.get('read')
    query = {'receiver' : user}
    if cond != None: query['read'] = cond == 'true'
    messages = collection.find(query)
    parsed_messages = []
    for message in messages:
        #parse the message into a dict, with a string representation of the '_id' field.
        parsed_message = {k:v for k,v in message.items() if k != '_id'}
        parsed_message['_id'] = str(message['_id']) 
        parsed_messages.append(parsed_message)
    return {'messages' : parsed_messages}

def write_message(request,collection):
    '''
    Write a new message. 
    User specified in the header is the sender.
    Parameters in the request body are: the receiving user, message subject and message body.
    Returns the id of the new message.
    '''
    data = dict(request.form).copy()
    data['creation date'] = str(datetime.date(datetime.now()))
    data['read'] = False
    data['sender'] = request.headers.get('user')
    res = collection.insert_one(data)
    return str(res.inserted_id)

def read_one(request,collection):
    '''
    Reads one message. Sets the 'read' field of the message to true.
    User specified in the header is the receiver.
    If no message id was specified, reads the first message for this user.
    If the user is not the receiver of intended message, does nothing.
    '''
    res = collection.find_one_and_update(build_query(request,'read'), {'$set' : {'read' : True}})
    return str(res)

def delete_message(request,collection):
    '''
    Route for deleting one message.
    User specified in the header is the sender/receiver.
    If no message id was specified, deletes one message by this user.
    If the user is not the sender/receiver of intended message, does nothing.
    '''
    res = collection.find_one_and_delete(build_query(request,'delete'))
    return str(res)