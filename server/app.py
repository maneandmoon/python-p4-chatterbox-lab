from flask import Flask, request, make_response, jsonify, abort
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

# @app.route('/messages')
# def messages():
#     return ''

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

# GET /messages: returns an array of all messages as JSON, ordered by created_at in ascending order.
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    message_list = [message.to_dict() for message in messages]
    return jsonify(message_list), 200

    # return jsonify([message.to_dict() for message in messages]), 200

# POST /messages: creates a new message with a body and username from params, and returns the newly created post as JSON.
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json
    if not data or not 'body' in data or not 'username' in data:
        abort(400)
    
    message = Message(body=data['body'], username=data['username'])
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

# PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.json
    if 'body' in data:
        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict())
    else:
        abort(400)

# DELETE /messages/<int:id>: deletes the message from the database.
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 204

if __name__ == '__main__':
    app.run(port=5555)
