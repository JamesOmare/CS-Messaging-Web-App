from src import create_app
from src.config.config import Config

app = create_app(Config)

if __name__ == '__main__':
    app.run(port = 5007)