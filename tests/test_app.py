import pytest
import uuid

from revenue.api import app, db
from revenue.utils import loader, date_utils
from revenue.api.models import Receipt


@pytest.fixture(scope='session')
def test_app():
    """
    Creates an instance of the api.

    session scope
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    yield app


@pytest.fixture(scope='function')
def test_client(test_app):
    """
    Creates a client with a new request context.

    test scope
    """
    app_context = test_app.app_context()
    db.create_all()

    app_context.push()

    brand_mappings = {
        "?!?": "?!?",
        "NS": "352h67i328fh",
    }
    loader.load_brand_name_mappings(db, brand_mappings)

    yield test_app.test_client()

    db.session.remove()
    db.drop_all()




