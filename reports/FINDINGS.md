# Findings

- **4,338 customers** with known IDs.
- Snapshot: **2011-12-10**.
- Highest sample silhouette: **k=2**, score **0.425**.
- Seed sensitivity ARI at selected k: **1.000**.
- The demo compares all candidate k values from 2 through 6.

## How to interpret this

Clusters have no ground-truth labels: silhouette is not accuracy. The chosen solution has two broad groups; more clusters are alternatives, not automatically better. Seed stability is not stability over time. Monetary value excludes refunds. Business actions need prospective validation.

Reproduce with `python -m src.pipeline`. Source hash and methodology are in `DATA.md` and `README.md`.
