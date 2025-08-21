from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        logging.info(f"triggring the data ingestion part")
        
        
        training_pipeline_config_obj = TrainingPipelineConfig()
        data_ingestion_config_obj = DataIngestionConfig(training_pipeline_config_obj)
        DataIngestion_obj = DataIngestion(data_ingestion_config_obj)
        logging.info(f"Initiate the data Ingestion")
        data_ingestion_artifact = DataIngestion_obj.initiate_data_ingestion()
        logging.info(f"Data Ingestion completed")
        print(data_ingestion_artifact)
        
        data_validation_config_obj=DataValidationConfig(training_pipeline_config_obj) 
        data_validation= DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config_obj)
        logging.info(f"Initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(f"Data Validation completed")
        print(f"\n\n data_validation_artifact {data_validation_artifact}")
        
        logging.info("data Transformation started")
        data_transformation_config_obj = DataTransformationConfig(training_pipeline_config_obj)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config_obj)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(f"\n\n {data_transformation_artifact}")
        logging.info("data Transformation completed")
        
        
        logging.info("Model Training Started")
        model_trainer_config_obj = ModelTrainerConfig(training_pipeline_config_obj)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config_obj,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        print(f"\n\n {model_trainer_artifact}")
        logging.info("Model Training artifact created")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)