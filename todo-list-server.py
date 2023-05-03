
"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

# TO DO: Die Namen der Variablen in den JSOn-Objekten passen nicht mit denen in der Spezifikation überein


import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
entries = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_4_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting and deleting existing todo lists
@app.route('/to-do-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in entries if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200


# define endpoint for adding a new list
@app.route('/to-do-list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = uuid.uuid4()
    todo_lists.append(new_list)
    return jsonify(new_list), 200

# defining endpoint for adding an entry to an existing todo-list
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_new_entry(list_id):
    # Unwrap object
    new_entry = request.get_json(force=True)
    # Debug message
    print('This new entry will be added: {}'.format(new_entry))
    # Sifting through the todolists
    list_id = None
    for l in todo_lists:
        # If ID is found, set test variable to something other than NONE, create UUID and save the listID
        if l['id'] == list_id:
            list_id = l['id']
            new_entry['id'] = uuid.uuid4()
            new_entry['list'] = list_id
            break
    # Check: Does the list exist? Does the object have a name?
    if not list_id:
        abort(404)
    if new_entry['name'] == None:
        abort(400)
    # If not aborted, entry must be valid. Append to list and return
    entries.append(new_entry)
    return jsonify(new_entry), 200

@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT, DELETE'])
def handle_entry(list_id, entry_id):
    new_entry = None
    for e in entries:
        if e['id'] == entry_id and e['list'] == list_id:
            new_entry = e
            break
    if new_entry == None:
        abort (404)
    if request.method == 'PUT':
        if e['name'] == None or e['name'] == '':
            abort(400)
        entries[entry_id] = new_entry
        return jsonify(new_entry), 200
    # PUT methode muss hier erstellt werden    
    if request.method == 'DELETE':
        print('Deleting entry...')
        entries.remove(new_entry)
        return '', 200



if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
