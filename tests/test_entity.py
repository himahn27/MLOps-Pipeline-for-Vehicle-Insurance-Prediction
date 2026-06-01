from vehicle_insurance.entity.config_entity import DataIngestionConfig
from vehicle_insurance.entity.artifact_entity import DataIngestionArtifact


config = DataIngestionConfig()
print(config)

artifact = DataIngestionArtifact(
    train_file_path="artifacts/train.csv",
    test_file_path="artifacts/test.csv"
)
print(artifact)