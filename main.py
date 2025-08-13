from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        logging.info(f"triggring the data ingestion part")
        
        
        training_pipeline_config_obj = TrainingPipelineConfig()
        data_ingestion_config_obj = DataIngestionConfig(training_pipeline_config_obj)
        DataIngestion_obj = DataIngestion(data_ingestion_config_obj)
        
        data_ingestion_artifact = DataIngestion_obj.initiate_data_ingestion()
        print(data_ingestion_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)