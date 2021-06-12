import itertools
import logging

from csv import DictReader
from os import path

from revenue.app import date_utils, models

THIS_DIR = path.dirname(__file__)
BASE_DIR = path.dirname(path.dirname(THIS_DIR))
DATA_FILE = path.join(BASE_DIR, "data", "data.csv")
BRANCH_NAMES_TO_IDS = {
    "Nory Sushi": "352h67i328fh",
    "Nory Pizza": "345hngydkgs",
    "Nory Taco": "2hg8j32gw8g"
}

logger = logging.getLogger(__name__)


def get_csv_stream(file_path):
    """
    Reads a csv file and returns a stream of dict items
    :param file_path: location of data file
    :return: stream of csv rows as dicts
    """
    with open(file_path, newline='') as csvfile:
        reader = DictReader(csvfile)
        for item in reader:
            yield item


def get_receipt_stream(item_stream, brand_mappings):
    """
    Wraps a csv item stream and returns a Receipt stream
    :param item_stream:
    :param brand_mappings:
    :return:
    """
    good, bad = 0, 0
    for i, item in enumerate(item_stream):
        try:
            r = csv_item_to_receipt(item, brand_mappings)
            good += 1
            logger.info("Good Record #{}. Receipt ={}".format(good, r))
            yield r
        except (ValueError, KeyError) as e:
            bad += 1
            logger.warning("Bad Record #{}. Error = {}. Row Number ={}".format(bad, e, i+2))


def csv_item_to_receipt(item, brand_mappings):
    """
    Converts an item from csv stream to a receipt
    :param item: a csv dict item
    :param brand_mappings: mappings between branch name to id
    :return: Receipt object
    """
    branch_name = item["Company Name"]
    branch_id = brand_mappings.get(branch_name)
    if branch_id is None:
        raise ValueError("branch id cannot be found for '{}'".format(branch_name))

    value = float(item["Total"])
    if not value:
        raise ValueError("value cannot be '{}'".format(value))

    full_date = date_utils.from_csv_format(item["Finalized Date"])
    return models.Receipt.create(
        external_id=item["Receipt ID"],
        branch_id=branch_id,
        full_date=full_date,
        value=value,
    )


def load_receipts(db, receipt_stream, commit_size):
    """
    method to take a receipt stream and injects it into the DB

    :param db:
    :param receipt_stream:
    :param commit_size:

    :return:
    """
    chunk = itertools.islice(receipt_stream, commit_size)
    r = next(chunk, None)
    while r is not None:
        db.session.add(r)
        for receipt in chunk:
            db.session.add(receipt)
        db.session.commit()
        chunk = itertools.islice(receipt_stream, commit_size)
        r = next(chunk, None)


def load_brand_name_mappings(db, brand_mappings):
    """

    :param db:
    :param brand_mappings:
    :return:
    """
    db.session.add_all(
        [
            models.BrandMapping.from_id_to_name(_id, _name)
            for _name, _id in brand_mappings.items()
        ]
    )
    db.session.commit()


def load_data(db, brand_mappings: dict = None, item_stream=None, commit_size=1000):
    """

    :param db:
    :param brand_mappings:
    :param item_stream:
    :param commit_size:
    :return:
    """
    brand_mappings = brand_mappings or BRANCH_NAMES_TO_IDS
    load_brand_name_mappings(db, brand_mappings)

    item_stream = item_stream or get_csv_stream(DATA_FILE)
    receipt_stream = get_receipt_stream(item_stream, brand_mappings)
    load_receipts(db, receipt_stream, commit_size)

