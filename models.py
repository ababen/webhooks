from app import db
from sqlalchemy.dialects.postgresql import JSON


class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(255))
    payload = db.Column(JSON)

    def __init__(self, id, website, payload):
        self.id = id
        self.website = website
        self.payload = payload

    def __repr__(self):
        return '<id {}>'.format(self.id)