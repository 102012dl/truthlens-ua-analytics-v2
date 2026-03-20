#!/usr/bin/env python3
"""Verify ML model file availability (Render / local)."""
import os
import sys
from pathlib import Path

# Repo root when run as python scripts/check_model.py
ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    model_path = os.environ.get("MODEL_PATH", "artifacts/best_model.joblib")
    p = Path(model_path)
    if not p.is_absolute():
        p = ROOT / p
    if p.exists():
        size_mb = p.stat().st_size / 1024 / 1024
        print(f"OK: {p} ({size_mb:.1f} MB)")
        return 0
    print(f"WARNING: {p} not found - classifier uses rule-based fallback")
    print("To fix:")
    print("  1. Train/export model (e.g. notebooks/01_isot_fake_news_mlflow.ipynb) -> artifacts/best_model.joblib")
    print("  2. On Render: set env MODEL_PATH or upload artifact / use persistent disk")
    return 1


if __name__ == "__main__":
    sys.exit(main())
