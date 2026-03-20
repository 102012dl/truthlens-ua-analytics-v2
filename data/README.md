# Data directory

Large or licensed datasets are **not** committed to this repository.

## Bundled in repo

| Path | Description |
|------|-------------|
| `data/gold/demo_cases.csv` | Small gold evaluation set (31 rows) for dashboard / tests |

## Optional downloads (ISOT baseline)

Training the LinearSVC baseline on the **ISOT** (English) fake/real news dataset is documented in:

- `notebooks/01_isot_fake_news_mlflow.ipynb`
- `docs/DATASET_SETUP.md`

After download, place `Fake.csv` and `True.csv` under `data/` (or follow the notebook paths).

## Scripts

- `scripts/fetch_datasets.py` — helper hooks for fetching public datasets where permitted  
- `scripts/download_datasets.py` — present in **TruthLens-UA** legacy repo; this v2 repo may use `fetch_datasets.py` instead — see `docs/DATASET_SETUP.md`
