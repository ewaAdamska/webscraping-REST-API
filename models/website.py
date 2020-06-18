import uuid
from sqlalchemy.sql import func

from db import db


class WebsiteModel(db.Model):
    __tablename__ = 'websites'

    # We can add the same site multiple times, because behind the same url we can scrap different content
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String(150), nullable=False)
    uuid = db.Column(db.String(40), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    content = db.Column(db.String())

    pictures = db.relationship('PictureModel', lazy='dynamic', cascade="all, delete")

    def __init__(self, src):
        self.src = src
        self.uuid = str(uuid.uuid4())

    def json(self):
        return {
            'src': self.src,
            'uuid': self.uuid,
            'time': str(self.time_created),
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
