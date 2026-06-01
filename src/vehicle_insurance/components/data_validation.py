import pandas as pd
import yaml
import os

from vehicle_insurance.entity.config_entity import DataValidationConfig
from vehicle_insurance.entity.artifact_entity import DataValidationArtifact


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def read_yaml_file(self, file_path: str) -> dict:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def validate_columns(self, df: pd.DataFrame, expected_columns: list) -> bool:
        df_columns = list(df.columns)
        for column in expected_columns:
            if column not in df_columns:
                return False
        return True

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            # Load train and test datasets
            train_df = pd.read_csv(self.config.train_file_path)
            test_df = pd.read_csv(self.config.test_file_path)

            # Load schema
            schema = self.read_yaml_file(self.config.schema_file_path)
            expected_columns = schema["columns"]

            # Validate columns
            train_status = self.validate_columns(train_df, expected_columns)
            test_status = self.validate_columns(test_df, expected_columns)

            if train_status and test_status:
                return DataValidationArtifact(
                    validation_status=True,
                    message="Data validation successful. All required columns are present."
                )
            else:
                return DataValidationArtifact(
                    validation_status=False,
                    message="Data validation failed. Missing required columns."
                )

        except Exception as e:
            return DataValidationArtifact(
                validation_status=False,
                message=str(e)
            )