import pymongo
from flask import Flask, request, jsonify, make_response
import jwt
from datetime import datetime, timedelta
from flask.json import JSONEncoder
from bson import json_util, ObjectId
from functools import wraps


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj): return json_util.default(obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config['SECRET_KEY'] = 'cryptoispower'

client = pymongo.MongoClient(
    "mongodb+srv://akul:crypto@cart-cluster.3aew2.mongodb.net/shopping?retryWrites=true&w=majority")
db = client['shopping']
tab_users = db['users']
tab_cart = db['cart']


def token_check(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'jwt-token' in request.headers:
            token = request.headers['jwt-token']

        if not token:
            return jsonify({'message': 'Token in missing'}), 401

        try:
            data = jwt.decode(token, app.config.get('SECRET_KEY'))
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Signature expired. Please log in again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Token. Please log in again.'}), 401

        return func(user_id, *args, **kwargs)

    return decorated


@app.route('/cart', methods=['GET'])
@token_check
def get_all_items(user_id):
    items = []
    data = tab_cart.find({"user_id": user_id})
    if data == None:
        return jsonify({'message': 'Item not found'}), 401

    for item in tab_cart.find({"user_id": user_id}):
        items.append(item)

    return jsonify(items), 200


@app.route('/cart/<item_id>', methods=['GET'])
@token_check
def get_item(user_id, item_id):
    try:
        data = tab_cart.find_one(
            {"_id": ObjectId(item_id), "user_id": user_id})
        if data == None:
            return jsonify({'message': 'Item not found'}), 401
    except:
        return jsonify({'message': 'Something went wrong'}), 401
    item = {}
    for i in data:
        item[i] = data[i]
    return jsonify(item), 200


@ app.route('/cart', methods=['POST'])
@ token_check
def add_item(user_id):

    try:
        data = request.get_json()

        item = {
            'user_id': user_id,
            'product_name': data['name'],
            'product_price': data['price'],
            'product_quantity': data['quantity']
        }
        tab_cart.insert_one(item)

        return jsonify({'message': 'Item added to Cart'})
    except Exception as e:
        return make_response("Erroc Occured", 401, {'WWW-Authenticate': 'Check item'})


@ app.route('/cart/<item_id>', methods=['DELETE'])
@ token_check
def remove_item(user_id, item_id):
    count_before = tab_cart.count_documents({"user_id": user_id})
    tab_cart.delete_one({"_id": ObjectId(item_id), "user_id": user_id})
    count_now = tab_cart.count_documents({"user_id": user_id})
    if count_before != count_now:
        return jsonify({'message': 'Item removed from cart'}), 200

    return jsonify({"message": "Item not found"}), 401


@ app.route('/cart', methods=['DELETE'])
@ token_check
def empty_cart(user_id):
    tab_cart.delete_many({})
    return jsonify({"message": "All items removed"}), 200


@ app.route('/login')
def login():

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login Required'})

    user = {
        'user': auth.username,
        'password': auth.password,
        'login_time': datetime.utcnow().strftime("%d/%m/%Y, %H:%M:%S")
    }
    user_id = tab_users.insert_one(user).inserted_id

    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=2),
            'iat': datetime.utcnow(),
            'user_id': str(user_id)
        }
        token = jwt.encode(
            payload,
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    except:
        return make_response("Error Occured", 401, {'WWW-Authenticate': 'Check Credentials'})

    return jsonify({'token': token.decode('UTF-8')})


if __name__ == "__main__":
    app.run(debug=False, threaded=True)
