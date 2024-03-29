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


class TestValidation:

    def test_no_qp_is_bad_request(self, test_client):
        rv = test_client.get('/sales/hourly')
        assert rv.status == "400 BAD REQUEST"

    def test_no_start_is_bad_request(self, test_client):
        rv = test_client.get('/sales/hourly?end=18/05/2020&branch_id=352h67i328fh')
        assert rv.status == "400 BAD REQUEST"

    def test_bad_date_format_is_bad_request(self, test_client):
        rv = test_client.get('/sales/hourly?start=18/05/202&end=18/05/2020&branch_id=352h67i328fh')
        assert rv.status == "400 BAD REQUEST"

    def test_start_cannot_be_after_end(self, test_client):
        rv = test_client.get('/sales/daily?start=18/05/2020&end=17/05/2020&branch_id=352h67i328fh')
        assert rv.status == "400 BAD REQUEST"

    def test_no_such_branch_id(self, test_client):
        rv = test_client.get('/sales/hourly?start=18/05/2020&end=19/05/2020&branch_id=?')
        assert rv.status == "404 NOT FOUND"


b_day = date_utils.from_api_string("26/03/2021")


class TestHourly:

    def test_hourly_empty(self, test_client):
        rv = test_client.get('/sales/hourly?start=26/03/2021&end=26/03/2021&branch_id=?!?')
        assert rv.status == "200 OK"
        data = rv.json["data"]
        assert data["total"] == 0.0

    def test_hourly_total_single_record(self, test_client):
        add_receipt(branch_id="?!?", full_date=b_day, value=50.0)
        rv = test_client.get('/sales/hourly?start=26/03/2021&end=26/03/2021&branch_id=?!?')
        assert rv.status == "200 OK"
        data = rv.json["data"]
        assert data["total"] == 50.0

    def test_hourly_total_mult_record(self, test_client):
        add_receipt(branch_id="?!?", full_date=b_day, value=50.0)
        add_receipt(branch_id="?!?", full_date=b_day.replace(hour=10), value=70.0)
        add_receipt(branch_id="?!?", full_date=b_day.replace(hour=10, minute=10), value=70.0)
        rv = test_client.get('/sales/hourly?start=26/03/2021&end=26/03/2021&branch_id=?!?')
        assert rv.status == "200 OK"
        data = rv.json["data"]
        assert data["total"] == 190.0

    def test_hourly_breakdown_mult_record(self, test_client):
        add_receipt(branch_id="?!?", full_date=b_day, value=50.0)
        add_receipt(branch_id="?!?", full_date=b_day.replace(hour=10), value=70.0)
        add_receipt(branch_id="?!?", full_date=b_day.replace(hour=10, minute=10), value=70.0)
        rv = test_client.get('/sales/hourly?start=26/03/2021&end=26/03/2021&branch_id=?!?')
        assert rv.status == "200 OK"
        hourly_breakdown = rv.json["data"]["hourly_breakdown"]
        assert hourly_breakdown["10"] == 140


def add_receipt(branch_id="?!?", full_date=b_day, value=100.0):
    r = Receipt.create(
        external_id=str(uuid.uuid4()),
        branch_id=branch_id,
        full_date=full_date,
        value=value,
    )
    db.session.add(r)
    db.session.commit()




