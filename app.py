from flask import Flask, jsonify, make_response, Response, request
import base64
from flask_cors import CORS

from os import environ
from flask_session import Session
import requests


import xmlrpc.client

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = environ.get("SESSION_SECRET")



ses = Session(app)
CORS(app)

url = "http://127.0.0.1:8069"
db = "divisoria"
username = "test10@test.com"
password = "09084741500"


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db,username,password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

@app.route("/api/product", methods=['GET'])
def product():

    body = {
        "fields": ["name", "description", "price", "image"],
    }
    
    r = requests.post(url + '/api/product', json={"params": body})

    return r.json()['result']

@app.route("/api/product/<id>", methods=['GET'])
def get_product(id):

    body = {
        "fields": ["name", "description", "price", "image"],
        "domain": [("id", "=", id)]
    }
    
    r = requests.post(url + '/api/product', json={"params": body})

    return r.json()['result'][0]


@app.route("/api/signup", methods=['POST'])
def signup_user():
    body = {
        "name":request.json.get("name"),
        "login":request.json.get("login"),
        "password":request.json.get("password")
    }

    r = requests.post(url + '/api/signup', json={"params": body})
    
    return r.json()['result']


@app.route("/file/load/image/<product_id>", methods=['GET'])
def file_load_image(product_id):

    body = {
        "fields": ["image"],
        "domain": [("id", "=", product_id)]
    }
    
    r = requests.post(url + '/api/product', json={"params": body})
    
    image = r.json().get('result')[0].get('image')
    
    base64_image = image
    binary_image = base64.b64decode(base64_image)

    return Response(binary_image, content_type="image/jpeg")
    
if __name__ == '__main__':
    app.run(debug=True)