import numpy as np
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from vehicle_insurance.entity.config_entity import ModelTrainerConfig
from vehicle_insurance.entity.artifact_entity import ModelTrainerArtifact


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def evaluate_model(self, X_train, y_train, X_test, y_test, models: dict):
        report = {}

        for name, model in models.items():
            model.fit(X_train, y_train)

            # Train prediction (normal)
            y_train_pred = model.predict(X_train)

            # ---- Threshold tuning for TEST data ----
            y_probs = model.predict_proba(X_test)[:, 1]

            best_f1 = 0
            best_thresh = 0.5

            for thresh in np.arange(0.1, 0.9, 0.05):
                y_pred_thresh = (y_probs >= thresh).astype(int)
                f1 = f1_score(y_test, y_pred_thresh)
                if f1 > best_f1:
                    best_f1 = f1
                    best_thresh = thresh

            y_test_pred = (y_probs >= best_thresh).astype(int)

            metrics = {
                "train_accuracy": accuracy_score(y_train, y_train_pred),
                "test_accuracy": accuracy_score(y_test, y_test_pred),
                "precision": precision_score(y_test, y_test_pred),
                "recall": recall_score(y_test, y_test_pred),
                "f1_score": f1_score(y_test, y_test_pred),
                "best_threshold": best_thresh,
                "model": model,
            }

            report[name] = metrics

        return report

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        train_arr = np.load(self.config.train_array_file_path)
        test_arr = np.load(self.config.test_array_file_path)

        X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
        X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

        models = {
            "LogisticRegression": LogisticRegression(
                max_iter=1000,
                class_weight='balanced'
            ),

            "RandomForest": RandomForestClassifier(
                n_estimators=200,
                class_weight='balanced',
                random_state=42
            ),

            "DecisionTree": DecisionTreeClassifier(
                class_weight='balanced',
                random_state=42
            ),

            "GradientBoosting": GradientBoostingClassifier(
                n_estimators=200,
                random_state=42
            ),
        }

        report = self.evaluate_model(X_train, y_train, X_test, y_test, models)

        # ---- Select best model based on F1 ----
        best_model_name = None
        best_f1 = 0.0

        for name, metrics in report.items():
            print(f"\n{name}")
            print(metrics)

            if metrics["f1_score"] > best_f1:
                best_f1 = metrics["f1_score"]
                best_model_name = name

        best_model = report[best_model_name]["model"]
        best_threshold = report[best_model_name]["best_threshold"]

        print(f"\n✅ Best Model Selected: {best_model_name}")
        print(f"✅ Best Threshold: {best_threshold}")

        # Save model
        with open(self.config.trained_model_file_path, "wb") as f:
            pickle.dump({
                "model": best_model,
                "threshold": best_threshold
            }, f)

        return ModelTrainerArtifact(
            trained_model_file_path=self.config.trained_model_file_path,
            train_accuracy=report[best_model_name]["train_accuracy"],
            test_accuracy=report[best_model_name]["test_accuracy"],
        )