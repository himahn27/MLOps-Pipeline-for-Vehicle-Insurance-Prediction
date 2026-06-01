import os
import pickle
import numpy as np

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from vehicle_insurance.entity.config_entity import ModelEvaluationConfig
from vehicle_insurance.entity.artifact_entity import ModelEvaluationArtifact


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def evaluate(self, model, threshold, X_test, y_test):
        probs = model.predict_proba(X_test)[:, 1]
        y_pred = (probs >= threshold).astype(int)

        return {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
        }

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:

        # Load test data
        test_arr = np.load(self.config.test_array_file_path)
        X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

        # Load newly trained model
        with open(self.config.trained_model_file_path, "rb") as f:
            new_saved = pickle.load(f)

        new_model = new_saved["model"]
        new_threshold = new_saved["threshold"]

        new_metrics = self.evaluate(new_model, new_threshold, X_test, y_test)

        print("\n📊 New Model Metrics:", new_metrics)

        # Check if old production model exists
        if os.path.exists(self.config.production_model_file_path):
            with open(self.config.production_model_file_path, "rb") as f:
                old_saved = pickle.load(f)

            old_model = old_saved["model"]
            old_threshold = old_saved["threshold"]

            old_metrics = self.evaluate(old_model, old_threshold, X_test, y_test)

            print("\n📊 Old Production Model Metrics:", old_metrics)

            # Compare F1 score
            if new_metrics["f1_score"] <= old_metrics["f1_score"]:
                print("\n❌ New model is NOT better than production model.")
                return ModelEvaluationArtifact(
                    is_model_accepted=False,
                    improved_accuracy=False
                )

        # If no old model OR new model better
        print("\n✅ New model accepted as production model.")

        return ModelEvaluationArtifact(
            is_model_accepted=True,
            improved_accuracy=True
        )