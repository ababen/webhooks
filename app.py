from flask import Flask, request, url_for
#from flask_api import FlaskAPI, status, exceptions
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
db = SQLAlchemy(app)
# migrate = Migrate(app, db)


class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(255))
    payload = db.Column(db.Text)

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
"""
notes = {
    0: 'do the shopping',
    1: 'build the codez',
    2: 'paint the door',
}

def note_repr(key):
    return {
        'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
        'text': notes[key]
    }


@app.route('/', methods=['GET'])
def index():
    #return jsonify({'incoming': list(map(lambda dev: dev.serialize(), Incoming.query.all()))})
    return {'hello': 'world'}


@app.route('/', methods=['POST'])
def add_webhook():
    web = requests()
    print(web)
    return "Okay"

@app.route('/webhooks/', methods=['POST'])
def add_webhook():
    if not request.json or not 'website' in request.json:
        abort(400)
        web = request.json()
        #web = Incoming(request.json['website'])
        #db.session.add(web)
        #db.session.commit()
        #return jsonify({'incomding': web.serializa()}), 201
        print(web)
        return web

@app.route("/", methods=['GET', 'POST'])
def notes_list():

    if request.method == 'POST':
        note = str(request.data.get('text', ''))
        idx = max(notes.keys()) + 1
        notes[idx] = note
        return note_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(notes.keys())]


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    if request.method == 'PUT':
        note = str(request.data.get('text', ''))
        notes[key] = note
        return note_repr(key)

    elif request.method == 'DELETE':
        notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)
"""
if __name__ == "__main__":
    app.run(debug=True)