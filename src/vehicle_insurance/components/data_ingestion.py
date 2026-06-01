import os

import pandas as pd
from sklearn.model_selection import train_test_split

from vehicle_insurance.configuration.mongo_db_connection import MongoDBClient
from vehicle_insurance.data_access.projection import PROJECTION
from vehicle_insurance.entity.config_entity import DataIngestionConfig
from vehicle_insurance.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:
    def __init__(self, config: DataIngestionConfig = DataIngestionConfig()):
        self.config = config

        # Create artifacts directory if it doesn't exist
        os.makedirs(self.config.artifact_dir, exist_ok=True)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Read all documents from MongoDB and return as a pandas DataFrame.
        """
        client = MongoDBClient().client
        collection = client[
            self.config.database_name
        ][
            self.config.collection_name
        ]

        cursor = collection.find({}, PROJECTION)
        df = pd.DataFrame(list(cursor))

        return df

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Execute the complete data ingestion process.
        """
        # Load data from MongoDB
        df = self.export_collection_as_dataframe()
        print(f"Dataset shape: {df.shape}")

        # Split into train and test sets
        train_df, test_df = train_test_split(
            df,
            test_size=self.config.test_size,
            random_state=self.config.random_state,
            stratify=df["Response"]
        )

        # Save train and test CSV files
        train_df.to_csv(self.config.train_file_path, index=False)
        test_df.to_csv(self.config.test_file_path, index=False)

        print(f"Train file saved to: {self.config.train_file_path}")
        print(f"Test file saved to: {self.config.test_file_path}")

        # Return artifact object
        return DataIngestionArtifact(
            train_file_path=self.config.train_file_path,
            test_file_path=self.config.test_file_path
        )