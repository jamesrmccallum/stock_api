import os
import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

NAMESPACE = '/stocksocket'
NEW_STOCK_ADDED = 'Add new stock'
NEW_STOCK_BCAST = 'new stock broadcast'
CONNECT_ACK = 'Connect ack'
PORT = int(os.getenv('PORT'))


@app.route('/')
def index():
    return "Hello!"


@socketio.on(NEW_STOCK_ADDED, namespace=NAMESPACE)
def notify_listeners(message):
    print(message['symbol'])
    emit(NEW_STOCK_BCAST, {'symbol': message['symbol']}, broadcast=True)


@socketio.on('connect', namespace=NAMESPACE)
def test_connect():
    print('Client connected')
    emit(CONNECT_ACK, {'data': 'Connected'})


@socketio.on('disconnect', namespace=NAMESPACE)
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, port=PORT)
