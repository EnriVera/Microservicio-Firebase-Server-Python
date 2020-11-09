from flask import Flask, request, jsonify, Response
import pymongo
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#app.config['MONGO_URI'] = 'mongodb://localhost/MicroFirebaseFlask'
mongoDB = pymongo.MongoClient("mongo", 27017)
db = mongoDB.MicroFirebaseFlask

@app.route('/', methods=['GET'])
def get_Hello():
    response = json_util.dumps({"wellcome": "jesus"})

    return Response(response, mimetype='application/json')

@app.route('/phone_book', methods=['GET'])
def get_users():
    users = db.phone_book.find()
    response = json_util.dumps(users)

    return Response(response, mimetype='application/json')

@app.route('/phone_book/<id>', methods=['GET'])
def get_user_id(id):
    user = db.phone_book.find_one({"_id":ObjectId(id)})
    response_user = json_util.dumps(user)
    return Response(response_user, mimetype='application/json')

@app.route('/phone_book', methods=['POST'])
def post_users():
    idUser = request.json['idUser']
    username = request.json['username']
    lastname = request.json['lastname']
    number_phone = request.json['number_phone']
    if idUser and username and lastname and number_phone:
        id = db.phone_book.insert_one({'username': username, 'lastname': lastname, 'number_phone': number_phone, 'idUser':idUser})
        #return {'id_contact': str(id)}
        return Response(json_util.dumps({'id_contact': str(id.inserted_id)}), mimetype='application/json')
    return not_found()

@app.route('/phone_book/<id>', methods=['PUT'])
def put_users(id):
    username = request.json['username']
    lastname = request.json['lastname']
    number_phone = request.json['number_phone']

    if username and lastname and number_phone:
        db.phone_book.update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username,
            'lastname': lastname,
            'number_phone': number_phone,
        }})
        return jsonify({"message": "modified"})

    response_notfound = jsonify({"message": "verified the data"})
    response_notfound.status_code = 404
    return response_notfound


@app.route('/phone_book/<id>', methods=['DELETE'])
def delete_user(id):
    db.phone_book.delete_one({"_id":ObjectId(id)})
    return {'message': 'delete user'}


@app.errorhandler(404)
def not_found(error=None):
    response  = jsonify({
        'message': f'Not Found: ${request.url}',
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)