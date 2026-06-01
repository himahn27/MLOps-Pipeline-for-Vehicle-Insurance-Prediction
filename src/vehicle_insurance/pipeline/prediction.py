import pickle
import pandas as pd


class VehicleInsurancePredictor:
    def __init__(self, model_path):
        with open(model_path, "rb") as f:
            saved = pickle.load(f)

        self.model = saved["model"]
        self.threshold = saved["threshold"]

    def predict(self, X):
        probs = self.model.predict_proba(X)[:, 1]
        preds = (probs >= self.threshold).astype(int)
        return preds


class VehicleData:
    def __init__(self,
                 Gender,
                 Age,
                 Driving_License,
                 Region_Code,
                 Previously_Insured,
                 Vehicle_Age,
                 Vehicle_Damage,
                 Annual_Premium,
                 Policy_Sales_Channel,
                 Vintage):

        self.data = {
            "Gender": [Gender],
            "Age": [Age],
            "Driving_License": [Driving_License],
            "Region_Code": [Region_Code],
            "Previously_Insured": [Previously_Insured],
            "Vehicle_Age": [Vehicle_Age],
            "Vehicle_Damage": [Vehicle_Damage],
            "Annual_Premium": [Annual_Premium],
            "Policy_Sales_Channel": [Policy_Sales_Channel],
            "Vintage": [Vintage],
        }

    def get_dataframe(self):
        return pd.DataFrame(self.data)


class PredictionPipeline:
    def __init__(self):
        self.model_path = "saved_models/model.pkl"
        self.preprocessor_path = "artifacts/preprocessor.pkl"

    def predict(self, dataframe: pd.DataFrame):
        # Load preprocessor
        with open(self.preprocessor_path, "rb") as f:
            preprocessor = pickle.load(f)

        # Transform input
        data_transformed = preprocessor.transform(dataframe)

        # Use threshold-based predictor
        predictor = VehicleInsurancePredictor(self.model_path)

        prediction = predictor.predict(data_transformed)

        return prediction[0]