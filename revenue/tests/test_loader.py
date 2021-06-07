
from os import path
from unittest import TestCase

from revenue.app import loader

THIS_DIR = path.dirname(__file__)
SAMPLE_DATA_FILE = path.join(THIS_DIR, "data", "sample_data.csv")


class TestLoader(TestCase):
    def test_item_stream(self):
        stream = loader.get_csv_stream(SAMPLE_DATA_FILE)
        num_lines = len([_ for _ in stream])
        self.assertEqual(num_lines, 8)

    def test_receipt_stream(self):
        s = loader.get_receipt_stream(
            loader.get_csv_stream(
                SAMPLE_DATA_FILE
            )
        )
        receipts = [r for r in s]
        self.assertEqual(len(receipts), 8)
        r1 = receipts[0]
        self.assertEqual(r1.external_id, "352h67i328fh-72493550")
        self.assertEqual(r1.value, 108.45)

    def test_bad_receipts_empty_line(self):
        s = loader.get_receipt_stream(
            (
                {},
             )
        )
        receipts = [r for r in s]
        self.assertEqual(len(receipts), 0)

    def test_bad_receipts_bad_date(self):
        s = loader.get_receipt_stream(
            (
                {"Receipt ID": "111", "Company Name": "Nory Taco", "Finalized Date": "23/06/2", "Total": "20.34"},
             )
        )
        receipts = [r for r in s]
        self.assertEqual(len(receipts), 0)

    def test_bad_receipts_no_such_company(self):
        s = loader.get_receipt_stream(
            (
                {"Receipt ID": "111", "Company Name": "Nory", "Finalized Date": "23/06/21 17:09", "Total": "20.34"},
             )
        )
        receipts = [r for r in s]
        self.assertEqual(len(receipts), 0)
