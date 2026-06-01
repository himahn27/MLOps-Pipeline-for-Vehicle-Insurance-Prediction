from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str



@dataclass
class DataValidationArtifact:
    validation_status: bool
    message: str    

@dataclass
class DataTransformationArtifact:
    def __init__(self,
        transformed_train_file_path,
        transformed_test_file_path,
        preprocessor_file_path):

        self.transformed_train_file_path = transformed_train_file_path
        self.transformed_test_file_path = transformed_test_file_path
        self.preprocessor_file_path = preprocessor_file_path

        # ✅ ADD THESE TWO LINES
        self.train_array_file_path = transformed_train_file_path
        self.test_array_file_path = transformed_test_file_path

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_accuracy: float
    test_accuracy: float  


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: bool

class ModelPusherArtifact:
    def __init__(self, production_model_file_path: str):
        self.production_model_file_path = production_model_file_path        