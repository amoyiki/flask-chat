from flask import Flask,render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'
db = SQLAlchemy(app)


class History(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.String(500))


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    message = History(message=msg)
    db.session.add(message)
    db.session.commit()

    send(msg, broadcast=True)


@app.route('/')
def index():
    messages = History.query.all()

    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    db.create_all()
    socketio.run(app)
    