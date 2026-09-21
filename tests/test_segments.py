import json, unittest
from pathlib import Path
import pandas as pd
import numpy as np
from src.pipeline import make_rfm

ROOT = Path(__file__).resolve().parents[1]


class SegmentTests(unittest.TestCase):
    def test_frequency_counts_invoices_and_snapshot_uses_dates(self):
        sales = pd.DataFrame(
            {
                "InvoiceNo": ["A", "A", "B", "C"],
                "CustomerID": [1, 1, 1, None],
                "Sales": [10, 20, 5, 9],
                "InvoiceDate": pd.to_datetime(
                    [
                        "2011-01-01 10:00",
                        "2011-01-01 10:00",
                        "2011-01-03 15:00",
                        "2011-01-04 18:00",
                    ]
                ),
            }
        )
        rfm, snapshot = make_rfm(sales)
        self.assertEqual(len(rfm), 1)
        self.assertEqual(rfm.loc[1, "frequency"], 2)
        self.assertEqual(rfm.loc[1, "monetary"], 35)
        self.assertEqual(rfm.loc[1, "recency"], 2)
        self.assertEqual(str(snapshot.date()), "2011-01-05")

    def test_profiles_and_anonymous_points(self):
        d = json.loads((ROOT / "reports/analysis.json").read_text())
        for k, m in d["models"].items():
            self.assertEqual(len(m["centers"]), int(k))
            self.assertEqual(sum(p["customers"] for p in m["profiles"]), d["customers"])
            self.assertAlmostEqual(sum(p["share"] for p in m["profiles"]), 1)
        self.assertTrue(
            all(
                set(p) == {"recency", "frequency", "monetary", "cluster"}
                for p in d["points"]
            )
        )
        for p in d["points"]:
            x = (
                np.log1p([p[f] for f in d["features"]]) - np.array(d["mean"])
            ) / np.array(d["scale"])
            centers = np.array(d["models"][str(d["selected_k"])]["centers"])
            self.assertEqual(
                int(np.argmin(((centers - x) ** 2).sum(axis=1))), p["cluster"]
            )

    def test_selection_uses_reported_silhouette(self):
        d = json.loads((ROOT / "reports/analysis.json").read_text())
        self.assertEqual(
            d["selected_k"], max(d["comparisons"], key=lambda c: c["silhouette"])["k"]
        )


if __name__ == "__main__":
    unittest.main()
