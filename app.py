import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.picture import Picture, PictureList
from resources.website import Website, WebsiteList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('ABI_SECRET_KEY')
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # new endpoint /auth

api.add_resource(Website, '/website', '/website/<string:uuid>')
api.add_resource(Picture, '/item/<string:name>')
api.add_resource(WebsiteList, '/websites')
api.add_resource(PictureList, '/pictures')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)