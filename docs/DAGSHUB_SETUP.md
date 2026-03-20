# DagsHub MLflow Setup (truthlens-ua-analytics-v2)

1. Створіть акаунт на [DagsHub](https://dagshub.com).
2. Репозиторій: **truthlens-ua-analytics-v2** (або підключіть GitHub mirror).
3. **Settings → Access Tokens** — створіть токен з доступом до MLflow.
4. Змінні середовища (локально або CI):

```text
DAGSHUB_USER=102012dl
DAGSHUB_REPO=truthlens-ua-analytics-v2
MLFLOW_TRACKING_URI=https://dagshub.com/102012dl/truthlens-ua-analytics-v2.mlflow
```

5. Локальний запуск з DagsHub:

```bash
pip install dagshub mlflow
python scripts/mlflow_setup.py --dagshub
```

6. Локально без DagsHub (каталог `mlruns/` у репо):

```bash
python scripts/mlflow_setup.py
```

Деталі експериментів — у ноутбуках `notebooks/` та `docs/DATASET_SETUP.md`.
