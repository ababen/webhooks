import os

from flask import Flask, request, url_for
#from flask_api import FlaskAPI, status, exceptions
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import JSON


app = Flask(__name__)
app.config.from_pyfile('config.py')
#app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
db = SQLAlchemy(app)

print(os.environ['APP_SETTINGS'])

class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(255))
    payload = db.Column(JSON)

    def __repr__(self):
        return '<Website %s>' % self.website


class WebhoookSchema(ma.Schema):
    class Meta:
        fields = ("id", "website", "payload")

webhook_schema = WebhoookSchema()
webhooks_schema = WebhoookSchema(many=True)

class WebhookListResoource(Resource):
    def get(self):
        webhooks = Webhook.query.all()
        return webhooks_schema.dump(webhooks)
    
    def post(self):
        new_webhook = Webhook(
            id = request.json['id'],
            website = request.json['website'],
            payload = request.json['payload']
        )
        db.session.add(new_webhook)
        db.session.commit()
        return webhook_schema.dump(new_webhook)

api.add_resource(WebhookListResoource, '/webhooks')

if __name__ == "__main__":
    app.run(debug=True)