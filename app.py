import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

NAMESPACE = 'stocksocket'
NEW_STOCK_ADDED = 'new stock'
PORT = int(os.getenv('PORT'))


@app.route('/')
def index():
    return "Hello!"


@socketio.on('my event', namespace=NAMESPACE)
def test_message(message):
    emit('my response', {'data': message['data']})


@socketio.on('my broadcast event', namespace=NAMESPACE)
def notify_listeners(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace=NAMESPACE)
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace=NAMESPACE)
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, port=PORT)
