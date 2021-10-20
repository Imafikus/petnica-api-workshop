from flask import Flask, request, jsonify
from person import AllPersons, Person
import status_codes as StatusCodes

app = Flask(__name__)

all_persons = AllPersons(persons = [
    Person(id=1, name='Aleksa', surname='Tesic', status='assistant'),
    Person(id=2, name='Milan', surname='Todorovic', status='employee'),
    Person(id=3, name='Pera', surname='Peric', status='student')
])

@app.route('/')
def hello_world():
    return 'hello'
    
@app.route('/people', methods=['GET'])
def get_people():
    return all_persons.json(), StatusCodes.OK

@app.route('/people', methods=['POST'])
def post_person():
    try:
        print(f'request: {request.json}')
        new_person = Person.parse_obj(request.json)
    except:
        return jsonify('Invalid format', StatusCodes.BAD_REQUEST)
    
    all_persons.persons.append(new_person)
    return jsonify('Person added'), StatusCodes.OK

@app.route('/people/update_name/<id>', methods=['PATCH'])
def update_name(id):
    try:
        new_name = request.json['name']
        target_id = int(id)
    except:
        return jsonify('Invalid format', StatusCodes.BAD_REQUEST)

    person_found = False
    for person in all_persons.persons:
        if person.id == target_id:
            person.name = new_name
            person_found = True
    
    if not person_found:
        return jsonify('Person does not exist'), StatusCodes.NOT_FOUND
    
    return jsonify('Person updated'), StatusCodes.OK

@app.route('/people/<id>', methods=['DELETE'])
def delete_by_id(id):
    try:
        target_id = int(id)
    except:
        return jsonify('Invalid format', StatusCodes.BAD_REQUEST)

    person_found = False
    updated_persons = []
    for person in all_persons.persons:
        if person.id != target_id:
            updated_persons.append(person)
        else:
            person_found = True
    
    if not person_found:
        return jsonify('Person does not exist'), StatusCodes.NOT_FOUND
    
    all_persons.persons = updated_persons
    return jsonify('Person deleted'), StatusCodes.OK
    
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)