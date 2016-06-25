from bottle import route, run, get, delete, post, request, abort, default_app
import json
from pymongo import MongoClient
import os

uri = os.environ['OPENSHIFT_MONGODB_DB_URL']
print("Trying to connect to " + uri)
preference_collection = MongoClient(uri).prefsync.preferences

DOT_CHAR = "."
DOT_UNICODE = "\\uff0"


@post('/users/<user_id>/preferences.json')
def add_preference(user_id):
    pref_body = request.body.read().decode("utf-8")
    user_preference = json.loads(pref_body)
    print("storing information for user_id:" + user_id)
    data_to_update = {'user_id': user_id,
                      'preference': user_preference}
    upserted_record = preference_collection.update(
        {'user_id': user_id}, {"$set": data_to_update}, upsert=True)
    # return str(upserted_record.updatedExisting)


@post('/users/<user_id>/files/<file_name>/sync.json')
def add_file(user_id, file_name):
    body = request.json
    print(body)
    file_name = body['file_name'].replace(DOT_CHAR, DOT_UNICODE)
    data_to_store = {'user_id': user_id, 'file_name': file_name, 'content': body['content'], 'dir': body['dir']}
    upserted_file = preference_collection.update(
        {'user_id': user_id, 'file_name': file_name}, data_to_store, upsert=True)
    # return str(upserted_file.updatedExisting)


@delete('/users/<user_id>/preferences/destroy')
def delete_preference(user_id):
    preference_collection.delete({'user_id': user_id})


@get('/users/<user_id>/preferences.json')
def get_preference(user_id):
    user_pref = preference_collection.find_one({'user_id': user_id})
    if user_pref:
        return user_pref['preference']
    else:
        abort(404, "Preference Not Found")

@get('/users/<user_id>/files/<file_name>/content.json')
def get_file_content(user_id, file_name):
    file_content = request.body.read().decode("utf-8")
    file_name = file_name.replace(DOT_CHAR, DOT_UNICODE)
    data_to_fetch = {'user_id': user_id, 'file_name': file_name}
    result = preference_collection.find_one(data_to_fetch)
    if result:
        print("result found!!!!")
        return result['content']
    abort(404, "Preference Not Found")


@route('/ping')
def ping():
    print("Successful request....")
    return "Pong!"

application = default_app()

# application.run(host='localhost', port=8888, debug=True, reloader=True)
