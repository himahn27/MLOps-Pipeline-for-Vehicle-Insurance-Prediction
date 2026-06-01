from vehicle_insurance.components.data_ingestion import DataIngestion
from vehicle_insurance.entity.config_entity import DataIngestionConfig

from vehicle_insurance.components.data_validation import DataValidation
from vehicle_insurance.entity.config_entity import DataValidationConfig

from vehicle_insurance.components.data_transformation import DataTransformation
from vehicle_insurance.entity.config_entity import DataTransformationConfig

from vehicle_insurance.components.model_trainer import ModelTrainer
from vehicle_insurance.entity.config_entity import ModelTrainerConfig

from vehicle_insurance.components.model_evaluation import ModelEvaluation
from vehicle_insurance.entity.config_entity import ModelEvaluationConfig

from vehicle_insurance.components.model_pusher import ModelPusher
from vehicle_insurance.entity.config_entity import ModelPusherConfig


class TrainingPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        print("Starting Training Pipeline...")

        # ---------------- Data Ingestion ----------------
        data_ingestion = DataIngestion(DataIngestionConfig())
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print("Data Ingestion Completed Successfully!")

        # ---------------- Data Validation ----------------
        data_validation = DataValidation(DataValidationConfig())
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact.message)

        if not data_validation_artifact.validation_status:
            raise Exception("Data validation failed. Stopping pipeline.")

        # ---------------- Data Transformation ----------------
        data_transformation = DataTransformation(DataTransformationConfig())
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print("Data Transformation Completed Successfully!")

        # ---------------- Model Training ----------------
        model_trainer = ModelTrainer(ModelTrainerConfig())
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        print("Model Training Completed!")
        print(f"Train Accuracy: {model_trainer_artifact.train_accuracy}")
        print(f"Test Accuracy: {model_trainer_artifact.test_accuracy}")

        # ---------------- Model Evaluation ----------------
        eval_config = ModelEvaluationConfig(
            test_array_file_path=data_transformation_artifact.test_array_file_path,
            trained_model_file_path=model_trainer_artifact.trained_model_file_path,
            production_model_file_path="saved_models/model.pkl"
        )

        model_evaluation = ModelEvaluation(eval_config)
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

        print("Model Evaluation Completed!")
        print("Model Accepted:", model_evaluation_artifact.is_model_accepted)

        # ---------------- Model Pusher ----------------
        if model_evaluation_artifact.is_model_accepted:
            pusher_config = ModelPusherConfig(
                trained_model_file_path=model_trainer_artifact.trained_model_file_path,
                production_model_file_path="saved_models/model.pkl"
            )

            model_pusher = ModelPusher(pusher_config)
            model_pusher_artifact = model_pusher.initiate_model_pusher()

            print("Model Pushed to Production Successfully!")
            print("Production Model Path:", model_pusher_artifact.production_model_file_path)
        else:
           print("Model was not accepted. Not pushing to production.")

if __name__ == "__main__":
    obj = TrainingPipeline()
    obj.run_pipeline()        