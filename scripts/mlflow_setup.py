def setup_tracking(use_dagshub=False):
    if use_dagshub:
        import dagshub
        dagshub.init(
            repo_owner="102012dl",
            repo_name="truthlens-ua-analytics-v2",  # NEW REPO NAME
            mlflow=True
        )

if __name__ == "__main__":
    import mlflow
    setup_tracking(use_dagshub=False)
    mlflow.set_experiment("TruthLens-UA-Analytics-v2")
    print("Local MLFlow tracking setup complete. Use --dagshub to track remotely.")
