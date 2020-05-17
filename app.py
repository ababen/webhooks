import os

from flask import Flask, request, url_for
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
#app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

from models import Webhook

print(os.environ['APP_SETTINGS'])
print(os.environ['DATABASE_URL'])

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