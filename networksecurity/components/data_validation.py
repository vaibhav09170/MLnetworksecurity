import os
import sys
import pandas as pd

from scipy.stats import ks_2samp

from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    def Validation_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns : {number_of_columns}")
            logging.info(f"DataFrame has #{len(dataframe.columns)} columns")
            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validation_numerical_columns_exist(self, dataFrame:pd.DataFrame)->bool:
        try:
            #logging.info(f"DataFrame has {len(dataFrame.select_dtypes(exclude="object").columns)} of numerical columns")
            if len(dataFrame.select_dtypes(exclude="object").columns) <= 0:
                return True
            else: 
                return False
             
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def detect_dataset_drift(self, based_df, current_df, threshold=0.05)-> bool:
        try:
            status = True
            report = {}
            for column in based_df.columns:
                d1= based_df[column]
                d2 = current_df[column]
                is_sample_distr=ks_2samp(d1,d2)
                if threshold<is_sample_distr.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                
                report.update(
                    {
                        column:{
                            "P_value":float(is_sample_distr.pvalue),
                            "drift_status":is_found
                        }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            # create dir
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            ### read the data from train and test dataset
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            
            
            ### Valida the number of column
            status = self.Validation_number_of_columns(dataframe=train_df)
            if not status:
                error_message=f"Train Dataframe does not contain all columns. \n"
            status = self.Validation_number_of_columns(dataframe=test_df)
            if not status:
                error_message = f"Test dataframe does not contain all coulmns. \n " 
             
            ### check numerical columns exist or not 
            status = self.validation_numerical_columns_exist(dataFrame=train_df)
            if not status:
                error_message = f"Train Dataframe does not have numerical "
            status = self.validation_numerical_columns_exist(dataFrame=test_df)
            if not status:
                error_message = f"Test Dataframe does not have numerical"
            
            ## Check datadrift
            status=self.detect_dataset_drift(based_df=train_df,current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index = False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)