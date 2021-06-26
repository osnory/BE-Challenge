from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from revenue.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from revenue.api.models import Receipt
from revenue.api import routes


