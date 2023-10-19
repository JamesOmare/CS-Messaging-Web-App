from flask import Blueprint
from flask_login import current_user
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from ..utils.utils import socketio, db


chat_socket = Blueprint('chat_socket', __name__)


