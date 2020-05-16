from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Incoming(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(20))
    type = db.Column(db.String(20))

    def __init__(self, website):
        self.website = website

    def serialize(self):
        return {"id": self.id,
                "website": self.website}

## hello oleg

@app.route('/webhooks/', methods=['GET'])
def index():
    return jsonify({'incoming': list(map(lambda dev: dev.serialize(), Incoming.query.all()))})

@app.route('/webhooks/', methods=['POST'])
def add_webhook():
    if not request.json or not 'website' in request.json:
        abort(400)
        web = Incoming(request.json['website'])
        db.session.add(web)
        db.session.commit()
        return jsonify({'incomding': web.serializa()}), 201


if __name__ == '__main__':
    app.run()
