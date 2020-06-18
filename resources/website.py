from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.website import WebsiteModel
from models.picture import PictureModel

from web_scraping import scrap_images, scrap_text


class Website(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'src',
        type=str,
        required=True,
        help="Website's address is needed."
    )

    def get(self, uuid):
        website = WebsiteModel.find_by_uuid(uuid)
        if website:
            return website.json()
        return {'message': f'Website was not found.'}, 404

    def post(self):
        payload = Website.parser.parse_args()
        # check if this website resource was already created
        site = WebsiteModel.find_by_src(src=payload['src'])
        if site:
            return {"message": f"The site {payload['src']} was already posted."}
        # create website model and save it to db
        site = WebsiteModel(**payload)
        try:
            site.save_to_db()
        except:
            return {'message': 'An error occurred while creating the new site resource.'}, 500

        # scrapping site & adding pictures
        images = scrap_images(url=payload['src'])  # TODO: check if such picture already exists in the db by hashing it

        # save each picture info to the db
        for img in images:
            picture = PictureModel(**img, website_id=site.id)
            picture.save_to_db()

        return site.json(), 201

    def delete(self, uuid):
        website = WebsiteModel.find_by_uuid(uuid)
        if website:
            website.delete_from_db()
            return {'message': f"Website {website.json()['src']} was successfully deleted from the service."}
        return {'message': f"Website not found."}


class WebsiteList(Resource):
    def get(self):
        return {'sites': [site.json() for site in WebsiteModel.query.all()]}, 200