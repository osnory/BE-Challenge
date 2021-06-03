import pytest

from revenue.app import app
from revenue.app import db


@pytest.fixture(scope='session')
def test_app():
    """
    Creates an instance of the app.

    session scope
    """
    app.config['TESTING'] = True

    yield app


@pytest.fixture(scope='function')
def test_client(test_app):
    """
    Creates a client with a new request context.

    test scope
    """
    app_context = test_app.app_context()
    app_context.push()

    return test_app.test_client()


class TestRoutes:
    def test_index(self, test_client):
        """Test Index."""

        rv = test_client.get('/')
        assert {"hello": "Hello"} == rv.json

    def test_no_qp_is_bad_request(self, test_client):
        rv = test_client.get('/hourly')
        assert rv.status == "400 BAD REQUEST"

    def test_no_start_is_bad_request(self, test_client):
        rv = test_client.get('/hourly?end=18/05/2020&branch_id=90')
        assert rv.status == "400 BAD REQUEST"

    def test_bad_date_format_is_bad_request(self, test_client):
        rv = test_client.get('/hourly?start=18/05/202&end=18/05/2020&branch_id=90')
        assert rv.status == "400 BAD REQUEST"
