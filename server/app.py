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

@app.route('/messages')
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    message_list = [{"id": msg.id, "username": msg.username, "body": msg.body, "created_at": msg.created_at} for msg in messages]
    return jsonify(message_list)


@app.route('/messages/<int:id>')
def messages_by_id(id):
    data = request.get_json()
    username = data.get('username')
    body = data.get('body')
    message = Message(username=username, body=body)
    db.session.add(message)
    db.session.commit()
    return jsonify({"message": "Message created successfully"}), 201


def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted successfully"})



if __name__ == '__main__':
    app.run(port=4000)
