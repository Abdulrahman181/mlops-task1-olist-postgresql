import os
import unittest
from unittest.mock import patch

import pandas as pd
from sqlalchemy.types import BigInteger, Text

from scripts import ingest


class IngestTests(unittest.TestCase):
    def test_database_url_is_required(self):
        with patch.dict(os.environ, {"DATABASE_URL": ""}):
            with self.assertRaisesRegex(RuntimeError, "DATABASE_URL is not set"):
                ingest.get_database_url()

    def test_database_url_is_read_from_environment(self):
        with patch.dict(os.environ, {"DATABASE_URL": "postgresql+psycopg2://example"}):
            self.assertEqual(
                ingest.get_database_url(), "postgresql+psycopg2://example"
            )

    def test_zip_code_prefix_is_text_and_keeps_leading_zeroes(self):
        frame = pd.DataFrame(
            {"customer_zip_code_prefix": pd.Series(["00123"], dtype="string")}
        )

        prepared = ingest.prepare_dataframe(frame)

        self.assertEqual(prepared.loc[0, "customer_zip_code_prefix"], "00123")
        self.assertIsInstance(
            ingest.get_sql_types(prepared.columns)["customer_zip_code_prefix"], Text
        )

    def test_quantity_column_remains_integer(self):
        self.assertIsInstance(ingest.get_sql_types(["order_item_id"])["order_item_id"], BigInteger)


if __name__ == "__main__":
    unittest.main()
