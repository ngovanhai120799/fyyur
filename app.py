from flask import Flask
from models import (
    create_app
)

app = Flask(__name__)
create_app(app)

if __name__ == '__main__':
    app.run()
