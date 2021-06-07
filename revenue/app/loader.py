import itertools
import logging

from csv import DictReader
from os import path

from revenue.app import validations, date_utils, models

THIS_DIR = path.dirname(__file__)
BASE_DIR = path.dirname(path.dirname(THIS_DIR))
DATA_FILE = path.join(BASE_DIR, "data", "data.csv")
ZIP_FILE = path.join(BASE_DIR, "data", "data.csv.zip")


logger = logging.getLogger(__name__)


def csv_item_to_receipt(item):
    """
    Converts an item from csv stream to a receipt
    :param item: a csv dict item
    :return: Receipt object
    """
    branch_name = item["Company Name"]
    branch_id = validations.get_brand_id(branch_name)
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


def get_receipt_stream(item_stream):
    """
    Wraps a csv item stream and returns a Receipt stream
    :param item_stream:
    :return:
    """
    good, bad = 0, 0
    for i, item in enumerate(item_stream):
        try:
            r = csv_item_to_receipt(item)
            good += 1
            logger.info("Good Record #{}. Receipt ={}".format(good, r))
            yield r
        except (ValueError, KeyError) as e:
            bad += 1
            logger.warning("Bad Record #{}. Error = {}. Row Number ={}".format(bad, e, i+2))


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




