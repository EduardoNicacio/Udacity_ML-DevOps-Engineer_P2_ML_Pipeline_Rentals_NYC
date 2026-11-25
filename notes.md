# EDA checklist

Use this checklist while working in `EDA.ipynb`. It records the required observations without implementing the analysis for you.

- [x] Fetch the `sample.csv:latest` artifact from the `nyc_airbnb` W&B project and load it into a dataframe.
      — `wandb.init(project="nyc_airbnb", group="eda", save_code=True)` then
      `wandb.use_artifact("sample.csv:latest").file()` in the first code cell (20,000 rows, 16 columns).
- [x] Add Markdown cells that explain each exploration and cleaning decision.
      — 9 Markdown cells: numbered sections, a `### Findings` block, and the cleaning rationale.
- [x] Inspect missing values. Record that they are not imputed during this EDA because the inference pipeline must handle them later.
      — `df.info()` plus the `### Why the missing values are **not** imputed here` Markdown cell;
      only `name`, `host_name`, `last_review` and `reviews_per_month` are incomplete and are left untouched.
- [x] Treat the accepted nightly price range as inclusive: `$10 <= price <= $350`.
      — `min_price = 10`, `max_price = 350`, `df['price'].between(min_price, max_price)` keeps 19,001 of 20,000 rows.
- [x] Convert `last_review` from text to a datetime value.
      — `df['last_review'] = pd.to_datetime(df['last_review'])`, confirmed as `datetime64[ns]` in the re-inspection cell.
- [x] Re-run the profile or equivalent dataframe inspection after your changes.
      — post-cleaning inspection cell reports rows, price range, dtype and remaining missing values.
- [x] Finish the W&B run.
      — final code cell calls `run.finish()`.
- [x] Restart the notebook kernel, run all cells from top to bottom, and resolve any errors.
      — executed with `jupyter nbconvert --execute`; 14 cells, execution counts 1–5, **0 error outputs**.
- [x] Save the completed notebook as `EDA.ipynb` in the repository root.
      — `EDA.ipynb` sits next to `main.py` and `config.yaml` and is committed.
