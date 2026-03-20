# Dataset setup (NMVP2)

Follow these steps when you need full ISOT training data or optional HuggingFace datasets.

## 1. ISOT (English) — fake/real news

Used by `notebooks/01_isot_fake_news_mlflow.ipynb` for reproducing the LinearSVC + TF-IDF baseline (`artifacts/best_model.joblib`).

1. Open [Kaggle: fake-and-real-news-dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset) (Clément Bisaillon).
2. Accept the dataset terms and download the archive.
3. Extract **`Fake.csv`** and **`True.csv`** into the project root under `data/`:

   ```
   truthlens-ua-analytics-v2/
   └── data/
       ├── Fake.csv
       └── True.csv
   ```

4. Run the notebook from the repository root so paths `data/Fake.csv` and `data/True.csv` resolve.

**Note:** License is **CC BY-NC 4.0**. Do not redistribute the raw CSVs in this repo unless your use complies with the license.

If the files are missing, the notebook falls back to a tiny synthetic pair of sentences so the pipeline still runs (not for reporting metrics).

## 2. UA NLP A/B notebook (`notebooks/03_ua_nlp_training.ipynb`)

Перенесено з [TruthLens-UA](https://github.com/102012dl/TruthLens-UA/blob/main/notebooks/03_ua_nlp_training.ipynb). Може підвантажувати зовнішні датасети через `datasets` або працювати на демо-прикладах; для повного злиття з ISOT спочатку підготуйте `data/Fake.csv` та `data/True.csv` (див. п. 1).

## 3. Optional: UNLP 2025 shared task (HuggingFace)

Referenced in `notebooks/02_dataset_audit.ipynb`. Requires `datasets` / HuggingFace access and may be unavailable in offline environments. Failure is expected and documented in the notebook output.

## 4. Domain trust and demo gold

Generated or curated CSVs under `data/gold/` and `data/processed/` are described in `docs/thesis/DATASETS.md`.
