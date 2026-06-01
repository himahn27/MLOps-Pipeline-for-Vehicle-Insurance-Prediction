import pandas as pd
import numpy as np
import os
import pickle

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from vehicle_insurance.entity.config_entity import DataTransformationConfig
from vehicle_insurance.entity.artifact_entity import DataTransformationArtifact


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_preprocessor(self):
        categorical_cols = ["Gender", "Vehicle_Age", "Vehicle_Damage"]
        numerical_cols = [
            
            "Age",
            "Driving_License",
            "Region_Code",
            "Previously_Insured",
            "Annual_Premium",
            "Policy_Sales_Channel",
            "Vintage",
        ]

        num_pipeline = Pipeline(
            steps=[("scaler", StandardScaler())]
        )

        cat_pipeline = Pipeline(
            steps=[("encoder", OneHotEncoder(handle_unknown="ignore"))]
        )

        preprocessor = ColumnTransformer(
            [
                ("num", num_pipeline, numerical_cols),
                ("cat", cat_pipeline, categorical_cols),
            ]
        )

        return preprocessor

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        train_df = pd.read_csv(self.config.train_file_path)
        test_df = pd.read_csv(self.config.test_file_path)

        target_column = "Response"

        X_train = train_df.drop(columns=[target_column])
        y_train = train_df[target_column]

        X_test = test_df.drop(columns=[target_column])
        y_test = test_df[target_column]

        preprocessor = self.get_preprocessor()

        X_train_transformed = preprocessor.fit_transform(X_train)
        X_test_transformed = preprocessor.transform(X_test)

        train_arr = np.c_[X_train_transformed, y_train]
        test_arr = np.c_[X_test_transformed, y_test]

        os.makedirs("artifacts", exist_ok=True)

        train_path = "artifacts/train_transformed.npy"
        test_path = "artifacts/test_transformed.npy"

        np.save(train_path, train_arr)
        np.save(test_path, test_arr)

        with open(self.config.preprocessor_obj_file_path, "wb") as f:
            pickle.dump(preprocessor, f)

        return DataTransformationArtifact(
            transformed_train_file_path=train_path,
            transformed_test_file_path=test_path,
            preprocessor_file_path=self.config.preprocessor_obj_file_path,
        )