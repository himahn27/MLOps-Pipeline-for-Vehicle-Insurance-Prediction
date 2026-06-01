from dataclasses import dataclass
import os

@dataclass
class DataIngestionConfig:
    database_name: str = "vehicle_insurance"
    collection_name: str = "insurance_data"
    artifact_dir: str = "artifacts"
    train_file_path: str = "artifacts/train.csv"
    test_file_path: str = "artifacts/test.csv"
    test_size: float = 0.2
    random_state: int = 42




@dataclass
class DataValidationConfig:
    train_file_path: str = "artifacts/train.csv"
    test_file_path: str = "artifacts/test.csv"
    schema_file_path: str = os.path.join("config", "schema.yaml")   

@dataclass
class DataTransformationConfig:
    train_file_path: str = "artifacts/train.csv"
    test_file_path: str = "artifacts/test.csv"
    preprocessor_obj_file_path: str = "artifacts/preprocessor.pkl" 

@dataclass
class ModelTrainerConfig:
    train_array_file_path: str = "artifacts/train_transformed.npy"
    test_array_file_path: str = "artifacts/test_transformed.npy"
    trained_model_file_path: str = "artifacts/model.pkl"



@dataclass
class ModelEvaluationConfig:
    test_array_file_path: str
    trained_model_file_path: str
    production_model_file_path: str  

class ModelPusherConfig:
    def __init__(self,
                 trained_model_file_path: str,
                 production_model_file_path: str):
        self.trained_model_file_path = trained_model_file_path
        self.production_model_file_path = production_model_file_path      