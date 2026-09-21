"""Reproducible acquisition and explicit cleaning of UCI Online Retail."""

from pathlib import Path
import hashlib, json, urllib.request, zipfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"


def load_data():
    path = ROOT / "data/raw/online_retail.xlsx"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        archive = path.with_suffix(".zip")
        urllib.request.urlretrieve(URL, archive)
        with zipfile.ZipFile(archive) as z:
            name = next(n for n in z.namelist() if n.endswith(".xlsx"))
            path.write_bytes(z.read(name))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    cache = path.with_suffix(".csv.gz")
    marker = path.with_suffix(".sha256")
    if cache.exists() and marker.exists() and marker.read_text() == digest:
        df = pd.read_csv(
            cache,
            dtype={"InvoiceNo": str, "StockCode": str},
            parse_dates=["InvoiceDate"],
        )
    else:
        df = pd.read_excel(path, dtype={"InvoiceNo": str, "StockCode": str})
        df.to_csv(cache, index=False, compression="gzip")
        marker.write_text(digest)
    return df, digest


def clean_sales(raw):
    """Return positive sales only; mutually exclusive audit counts reconcile to input."""
    df = raw.copy()
    audit = {"raw_rows": int(len(df))}
    duplicates = df.duplicated()
    audit["duplicate_rows"] = int(duplicates.sum())
    df = df.loc[~duplicates].copy()
    cancellation = df["InvoiceNo"].astype(str).str.upper().str.startswith("C") | (
        df["Quantity"] < 0
    )
    audit["cancellation_or_negative_rows"] = int(cancellation.sum())
    df = df.loc[~cancellation].copy()
    invalid = (
        (df["Quantity"] <= 0)
        | (df["UnitPrice"] <= 0)
        | df["InvoiceDate"].isna()
        | df["Quantity"].isna()
        | df["UnitPrice"].isna()
    )
    audit["nonpositive_or_invalid_rows"] = int(invalid.sum())
    df = df.loc[~invalid].copy()
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    df["Country"] = df["Country"].fillna("Unknown")
    df["Description"] = df["Description"].fillna("Unknown item")
    df["Month"] = df["InvoiceDate"].dt.strftime("%Y-%m")
    audit["clean_rows"] = int(len(df))
    audit["missing_customer_rows_retained"] = int(df["CustomerID"].isna().sum())
    return df, audit


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False), encoding="utf-8")
