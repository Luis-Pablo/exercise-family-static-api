"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "menssage": "members family",
        "family": members
    }
    return jsonify(response_body), 200



@app.route('/members/<int:id>')
def get_member(id):
    members = jackson_family.get_member(id)
    response_body = {
        "menssage": "member id",
        "family": members
    }
   
    return jsonify(response_body), 200
  


@app.route('/members', methods=['POST'])
def create_member():
    new_member = {
        "id": jackson_family._generateId(),
        "first_name": request.json['first_name'],
        "age": request.json["age"],
        "last_name": "Jackson",
        "lucky_numbers": request.json["lucky_numbers"]
    }
    
    jackson_family.add_member(new_member)
    return jsonify({'message': 'create new member'})


@app.route('/members', methods=['DELETE'])
def delete():
    member = jackson_family.delete_member()
    response_body = {
        "menssage": "member family delete",
        "family": member
    }
    return jsonify(response_body), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
