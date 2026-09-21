# Study guide: Customer Segmentation Lab

## Read in this order

1. Try the demo and change several inputs.
2. Read the question, method, and limitations in README.md.
3. Run every cell of notebooks/analysis.ipynb.
4. Trace a displayed result back to src/pipeline.py and its raw data.
5. Read the tests and change one assumption in a new experiment.

## Be ready to explain

- Why does frequency count invoices instead of rows?
- Why transform skewed RFM features before K-means?
- Why is silhouette not classification accuracy?
- What does the second-seed ARI check, and what does it not check?
- Why are two segments selected even though more detailed groups may sound appealing?
- How could you validate stability over time and the value of marketing actions?

## Make it your own

Write a one-page interpretation in your own words, implement one of the notebook extension ideas, and record both what improved and what did not. Keep a new test period for any supervised model changes. Do not claim business impact, accuracy, or independent authorship that the evidence does not support.
