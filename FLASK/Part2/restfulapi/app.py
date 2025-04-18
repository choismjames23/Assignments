from flask import Flask
from flask_restful import Api
from resources.item import Item

app = Flask(__name__)

api = Api(app)

#경로 추가
api.add_resource(Item, '/item/<string:name>') 