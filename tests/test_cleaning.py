import unittest
import pandas as pd
from src.data import clean_sales


class CleaningTests(unittest.TestCase):
    def test_mutually_exclusive_audit_and_unknown_customers(self):
        row = {
            "InvoiceNo": "1",
            "StockCode": "A",
            "Description": "item",
            "Quantity": 2,
            "UnitPrice": 3.0,
            "InvoiceDate": pd.Timestamp("2011-01-01"),
            "CustomerID": 123.0,
            "Country": "UK",
        }
        rows = [
            row,
            row.copy(),
            dict(row, InvoiceNo="C2", Quantity=-2),
            dict(row, InvoiceNo="3", Quantity=-1),
            dict(row, InvoiceNo="4", UnitPrice=0),
            dict(row, InvoiceNo="5", CustomerID=None),
        ]
        sales, audit = clean_sales(pd.DataFrame(rows))
        self.assertEqual(audit["raw_rows"], 6)
        self.assertEqual(audit["duplicate_rows"], 1)
        self.assertEqual(audit["cancellation_or_negative_rows"], 2)
        self.assertEqual(audit["nonpositive_or_invalid_rows"], 1)
        self.assertEqual(audit["clean_rows"], 2)
        self.assertEqual(audit["missing_customer_rows_retained"], 1)
        self.assertEqual(sales.Sales.sum(), 12.0)
        self.assertEqual(
            sum(
                audit[k]
                for k in [
                    "duplicate_rows",
                    "cancellation_or_negative_rows",
                    "nonpositive_or_invalid_rows",
                    "clean_rows",
                ]
            ),
            audit["raw_rows"],
        )


if __name__ == "__main__":
    unittest.main()
