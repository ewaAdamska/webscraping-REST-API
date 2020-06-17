from db import db
import uuid



class WebsiteModel(db.Model):
    __tablename__ = 'websites'

    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String(150), nullable=False)
    uuid = db.Column(db.String(40), nullable=False)
    # TODO: add timestamp info, page text etc

    pictures = db.relationship('PictureModel', lazy='dynamic')

    def __init__(self, src):
        self.src = src
        self.uuid = str(uuid.uuid4())

    def json(self):
        return {
            'src': self.src,
            'uuid': self.uuid,
            'pictures': [picture.json() for picture in self.pictures.all()]
        }

    @classmethod
    def find_by_src(cls, src):
        return cls.query.filter_by(src=src).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
