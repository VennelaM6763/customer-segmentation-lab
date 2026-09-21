# Data provenance

Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33.

License: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution applies to included derived figures, aggregates, model inputs, and demo data. The MIT license covers the authored code, not the underlying data.

Downloaded on 20 September 2026 from the UCI repository. Raw data are excluded from Git and the portable ZIP. The pipeline downloads them if missing and preserves a local cache for subsequent runs.

SHA-256 of the raw Excel workbook used for the included results:

`43465a06f2ccf7c8b5bd2892bc7defb52f97487934fe93b16ae4c3936424676d`

The included results use 541,909 original transaction rows from 1 December 2010 to 9 December 2011. The cleaning audit, exclusion rules and missing-customer counts are recorded in reports/analysis.json. Monetary values are GBP; IDs are treated as identifiers. Exports omit customer IDs.

Derived data include positive-sales aggregates and/or log-transformed, standardized RFM cluster profiles. No claims are made about the retailer today.
