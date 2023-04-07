from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        response = make_response(
            jsonify([message.to_dict() for message in messages])
            , 200)
        
    elif request.method == 'POST':
        new_message = request.get_json()
        message = Message(
            body= new_message['body'],
            username = new_message['username']
        )

        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message.to_dict()), 
            201,
        )

    return response

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()

    if request.method == "PATCH":
        new_message = request.get_json()
        for line in new_message:
            setattr(message, line, new_message[line])

        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message.to_dict()),
            200
            )
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        response = make_response(
             jsonify({'deleted': True}), 
             200
             )
    return response

if __name__ == '__main__':
    app.run(port=5555)
