import os
import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

NAMESPACE = '/stocksocket'
NEW_STOCK_ADDED = 'new stock'
NEW_STOCK_BCAST = 'new stock broadcast'
CONNECT_ACK = 'Connect ack'
PORT = int(os.getenv('PORT'))


@app.route('/')
def index():
    return "Hello!"


@socketio.on('my event', namespace=NAMESPACE)
def test_message(message):
    emit('my response', {'data': message['data']})


def notify_listeners(message):
    emit(NEW_STOCK_BCAST, {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace=NAMESPACE)
def test_connect():
    logging.info('Client connected')
    emit(CONNECT_ACK, {'data': 'Connected'})


@socketio.on('disconnect', namespace=NAMESPACE)
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, port=PORT)
