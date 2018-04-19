import os
import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

NAMESPACE = '/stocksocket'
NEW_STOCK_ADDED = 'Add new stock'
NEW_STOCK_BCAST = 'new stock broadcast'
STOCK_REMOVED = 'Stock removed'
STOCK_REMOVED_BCAST = 'stock removed broadcast'
CONNECT_ACK = 'Connect ack'
PORT = int(os.getenv('PORT'))


@app.route('/')
def index():
    return "Hello!"


@socketio.on(NEW_STOCK_ADDED, namespace=NAMESPACE)
def bcast_new_stock(message):
    emit(NEW_STOCK_BCAST, {'symbol': message['symbol']}, broadcast=True)


@socketio.on(STOCK_REMOVED, namespace=NAMESPACE)
def bcast_stock_remove(message):
    emit(STOCK_REMOVED_BCAST, {'symbol': message['symbol']}, broadcast=True)


@socketio.on('connect', namespace=NAMESPACE)
def test_connect():
    emit(CONNECT_ACK, {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, port=PORT)
