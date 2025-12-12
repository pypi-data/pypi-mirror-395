import time


class DumyTrainerApp:

    def __init__(self):
        pass

    def train(self, train_input)-> dict:
        time.sleep(15)
        return {"model_version": "v1", "records_trained": 100000, "accuracy": 1.42325732, "precision": 1.2123890, "recall": 2.136233, "f1_score": 1.3864742, "model_artifact_path": r"D:\working\evol-aiq\artifacts\model_registry\churn\lightgbm\v1", "error_message": "all ok"}