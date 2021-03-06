from flask import Flask, request, jsonify
from person import Course, Person
import status_codes as StatusCodes
import requests
from pydantic import BaseModel

app = Flask(__name__)

course = Course(people = [
    Person(id=1, name='Aleksa', surname='Tesic', status='assistant'),
    Person(id=2, name='Milan', surname='Todorovic', status='employee'),
    Person(id=3, name='Pera', surname='Peric', status='student'),
    Person(id=4, name='Pera', surname='Peric', status='student')
    
])

class TimeServiceResponse(BaseModel):
    current_time: str


@app.route('/', methods=['GET'])
def hello_world():
    return f'hello exact time is: ', StatusCodes.OK

@app.route('/time', methods=['GET'])
def get_time():
    try:
        res = requests.get('http://127.0.0.1:5001/time', timeout=3)
        if res.status_code != StatusCodes.OK:
            raise Exception()
    except:    
        return 'Service unavailable', StatusCodes.SERVICE_UNAVAILABLE
    
    try:
        data: TimeServiceResponse = TimeServiceResponse.parse_obj(res.json())
    except:
        return 'Unexpected error', StatusCodes.INTERNAL_SERVER_ERROR
    
    return f'Currrent time is {data.current_time}', StatusCodes.OK


@app.route('/people', methods=['GET'])
def get_all_people():
    return course.json(), StatusCodes.OK

@app.route('/people', methods=['POST'])
def post_person():
    try:
        print(f'request: {request.json}')
        new_person = Person.parse_obj(request.json)
    except:
        return jsonify('Invalid format'), StatusCodes.BAD_REQUEST
    
    course.people.append(new_person)
    return jsonify('Person added'), StatusCodes.OK

@app.route('/people/update_name/<id>', methods=['PATCH'])
def update_name_by_id(id):
    try:
        new_name = request.json['name']
        target_id = int(id)
    except:
        return jsonify('Invalid format'), StatusCodes.BAD_REQUEST

    person_found = False
    for person in course.people:
        if person.id == target_id:
            person.name = new_name
            person_found = True
    
    if not person_found:
        return jsonify('Person does not exist'), StatusCodes.NOT_FOUND
    
    return jsonify('Person updated'), StatusCodes.OK

@app.route('/people/<id>', methods=['DELETE'])
def delete_people_by_id(id):
    try:
        target_id = int(id)
    except:
        return jsonify('Invalid format'), StatusCodes.BAD_REQUEST

    person_found = False
    updated_people = []
    for person in course.people:
        if person.id != target_id:
            updated_people.append(person)
        else:
            person_found = True
    
    if not person_found:
        return jsonify('Person does not exist'), StatusCodes.NOT_FOUND
    
    course.people = updated_people
    return jsonify('Person deleted'), StatusCodes.OK

@app.route('/people/search/', methods=['GET'])
def get_people_by_name_status():
    target_name = request.args.get('name')
    target_status = request.args.get('status')
    
    if target_name is None or target_status is None:
        return 'Name and status must be defined.', StatusCodes.BAD_REQUEST
    
    filtered_people = Course()
    for p in course.people:
        if p.name == target_name and p.status == target_status:
            filtered_people.people.append(p)
    
    return filtered_people.json(), StatusCodes.OK


if __name__ == '__main__':
    app.run(debug=True, port=5000)