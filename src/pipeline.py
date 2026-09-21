"""Customer RFM clustering, candidate comparison, and portable model export."""

import json
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.preprocessing import StandardScaler
from .data import ROOT, load_data, clean_sales, save_json

FEATURES = ["recency", "frequency", "monetary"]


def make_rfm(sales):
    known = sales.dropna(subset=["CustomerID"])
    snapshot = sales.InvoiceDate.max().normalize() + pd.Timedelta(days=1)
    rfm = known.groupby("CustomerID").agg(
        last_purchase=("InvoiceDate", "max"),
        frequency=("InvoiceNo", "nunique"),
        monetary=("Sales", "sum"),
    )
    rfm["recency"] = (snapshot - rfm.last_purchase.dt.normalize()).dt.days
    return rfm[FEATURES], snapshot


def main():
    raw, digest = load_data()
    sales, audit = clean_sales(raw)
    rfm, snapshot = make_rfm(sales)
    scaler = StandardScaler()
    X = scaler.fit_transform(np.log1p(rfm[FEATURES]))
    models, comparisons = {}, []
    for k in range(2, 7):
        model = KMeans(n_clusters=k, n_init=20, random_state=42).fit(X)
        alternate = KMeans(n_clusters=k, n_init=20, random_state=7).fit(X)
        score = float(
            silhouette_score(
                X, model.labels_, sample_size=min(2000, len(X)), random_state=42
            )
        )
        stability = float(adjusted_rand_score(model.labels_, alternate.labels_))
        comparisons.append(
            {
                "k": k,
                "silhouette": score,
                "seed_stability_ari": stability,
                "inertia": float(model.inertia_),
            }
        )
        profiles = []
        labeled = rfm.assign(cluster=model.labels_)
        for label, g in labeled.groupby("cluster"):
            profiles.append(
                {
                    "id": int(label),
                    "customers": int(len(g)),
                    "share": float(len(g) / len(rfm)),
                    "recency": float(g.recency.median()),
                    "frequency": float(g.frequency.median()),
                    "monetary": float(g.monetary.median()),
                    "total_sales": float(g.monetary.sum()),
                }
            )
        models[str(k)] = {
            "centers": model.cluster_centers_.tolist(),
            "profiles": profiles,
        }
    selected = max(comparisons, key=lambda c: c["silhouette"])["k"]
    labels = KMeans(n_clusters=selected, n_init=20, random_state=42).fit_predict(X)
    sample = rfm.assign(cluster=labels).sample(n=min(1200, len(rfm)), random_state=42)
    # Export anonymous points only: customer IDs are unnecessary for the demo.
    points = [
        {
            "recency": int(r.recency),
            "frequency": int(r.frequency),
            "monetary": round(float(r.monetary), 2),
            "cluster": int(r.cluster),
        }
        for r in sample.itertuples()
    ]
    data = {
        "project": "segments",
        "source": "UCI Online Retail",
        "sha256": digest,
        "audit": audit,
        "snapshot": str(snapshot.date()),
        "customers": len(rfm),
        "selected_k": selected,
        "features": FEATURES,
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
        "models": models,
        "comparisons": comparisons,
        "points": points,
        "ranges": {f: [float(rfm[f].min()), float(rfm[f].max())] for f in FEATURES},
    }
    save_json(ROOT / "reports/analysis.json", data)
    pd.DataFrame(comparisons).to_csv(
        ROOT / "reports/cluster_comparison.csv", index=False
    )
    pd.DataFrame(models[str(selected)]["profiles"]).to_csv(
        ROOT / "reports/segment_profiles.csv", index=False
    )
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6))
    axs[0].plot(
        [c["k"] for c in comparisons],
        [c["silhouette"] for c in comparisons],
        "o-",
        color="#7742cc",
    )
    axs[0].set(
        xlabel="Number of clusters",
        ylabel="Sample silhouette",
        title="Compare candidate segmentations",
        xticks=range(2, 7),
    )
    axs[1].scatter(
        sample.frequency,
        sample.monetary,
        c=sample.cluster,
        cmap="viridis",
        s=12,
        alpha=0.5,
    )
    axs[1].set(
        xscale="log",
        yscale="log",
        xlabel="Orders (log scale)",
        ylabel="Positive spend, GBP (log scale)",
        title=f"Selected k={selected}; 1,200-customer sample",
    )
    fig.tight_layout()
    fig.savefig(ROOT / "reports/segments.png", dpi=160)
    plt.close(fig)
    (ROOT / "demo/data.js").write_text(
        "window.PROJECT_DATA=" + json.dumps(data, allow_nan=False) + ";",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"customers": len(rfm), "selected_k": selected, "comparisons": comparisons},
            indent=2,
        )
    )
    return data


if __name__ == "__main__":
    main()
