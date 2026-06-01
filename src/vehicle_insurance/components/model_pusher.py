import os
import shutil

from vehicle_insurance.entity.config_entity import ModelPusherConfig
from vehicle_insurance.entity.artifact_entity import ModelPusherArtifact


class ModelPusher:
    def __init__(self, config: ModelPusherConfig):
        self.config = config

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Push the trained model to production (saved_models folder)
        """

        os.makedirs(os.path.dirname(self.config.production_model_file_path), exist_ok=True)

        # Copy accepted model to production location
        shutil.copy(
            self.config.trained_model_file_path,
            self.config.production_model_file_path
        )

        return ModelPusherArtifact(
            production_model_file_path=self.config.production_model_file_path
        )