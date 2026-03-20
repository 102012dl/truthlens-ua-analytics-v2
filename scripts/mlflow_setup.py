#!/usr/bin/env python3
"""Configure MLflow tracking for truthlens-ua-analytics-v2 (local or DagsHub)."""
from __future__ import annotations

import argparse
from pathlib import Path


def setup_tracking(use_dagshub: bool = False) -> None:
    """Configure MLflow tracking for truthlens-ua-analytics-v2."""
    if use_dagshub:
        try:
            import dagshub

            dagshub.init(
                repo_owner="102012dl",
                repo_name="truthlens-ua-analytics-v2",
                mlflow=True,
            )
            print("[mlflow] DagsHub: truthlens-ua-analytics-v2")
        except ImportError:
            print("[mlflow] dagshub not installed — falling back to local tracking")
            setup_tracking(use_dagshub=False)
        return

    import mlflow

    root = Path("mlruns").resolve()
    root.mkdir(exist_ok=True)
    mlflow.set_tracking_uri(root.as_uri())
    mlflow.set_experiment("truthlens-ua-analytics-v2")
    print("[mlflow] Local:", root)


def main() -> None:
    p = argparse.ArgumentParser(description="MLflow setup for NMVP2")
    p.add_argument(
        "--dagshub",
        action="store_true",
        help="Use DagsHub remote tracking (requires dagshub + token)",
    )
    args = p.parse_args()
    setup_tracking(use_dagshub=args.dagshub)
    print("Done.")


if __name__ == "__main__":
    main()
