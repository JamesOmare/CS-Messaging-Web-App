from doctest import debug
from src import create_app, socketio
from src.config.config import Config

app = create_app(Config)

if __name__ == '__main__':
    socketio.run(app, port = 5007)