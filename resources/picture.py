from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.picture import PictureModel


class Picture(Resource):

    def get(self, _id):
        item = PictureModel.find_by_id(_id)
        if item:
            return item.json()
        return {'message': 'Picture not found'}, 404

    def delete(self, _id):
        item = PictureModel.find_by_id(_id)
        if item:
            item.delete_from_db()
        return {'message': 'Picture successfully deleted'}


class PictureList(Resource):
    def get(self):
        return {'pictures': [picture.json() for picture in PictureModel.query.all()]}, 200

