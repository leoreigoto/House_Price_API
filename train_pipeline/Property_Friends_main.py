"""
Main module for the 'Property_Friends' machine learning pipeline.

This module implements the main functionality for the Property Friends machine learning pipeline. It includes
the integration of various components such as data loading, logging, configuration management, and the 
execution of the MLFlow pipeline for model training, evaluation, and saving. It integrates with MLflow for
experiment tracking and model management.

The pipeline is specifically designed for the House Price Prediction use case, utilizing the Gradient Boosting
Regressor algorithm. It leverages custom utility modules for configuration loading, logging, model evaluation,
and MLFlow-based training and evaluation.

Constants:

    - MODULE_NAME: Name of the current module for logging purposes.
    - LOGGER_LEVEL: Logging level.
    - EXPERIMENT_NAME: Name of the MLFlow experiment.
    - MODEL_NAME: Name of the machine learning model.
    - TAGS: Tags for MLFlow logging.
    - RUN_NAME: Name of the MLFlow run
    - CONFIG_PATH: Path to load the config file
    - RANDOM_SEED: Fix a random seed to make the code reproducible
"""

import logging
from datetime import datetime

#custom imports
from create_logger import get_logger
from config_train_loader import load_train_config
from Property_Friends_mlflow_train_eval import train_evaluate_mlflow
from Property_Friends_data_loader import load_data_csv, load_data_sql


#constants
MODULE_NAME  = 'Property_Friends_main'
LOGGER_LEVEL = logging.INFO
EXPERIMENT_NAME = "House Price Prediction"
MODEL_NAME = "basic-GradientBoostingRegressor"  
TAGS={"tag1":"House Price Prediction", "tag2":"GradientBoostingRegressor"}
RUN_NAME= f"House_{datetime.now().strftime('''%Y-%m-%d_%H-%M-%S''')}"
CONFIG_PATH='config.json'
RANDOM_SEED=42

#Train with mlflow and saving in a sqlite DB
#need to start mlflow server
#cmd: mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 127.0.0.1 --port 5000
MLFLOW_TRACKING_URI='http://127.0.0.1:5000'

 
def main():
    """
    Main function to execute the machine learning pipeline.

    This function initializes logging, loads configuration, 
    reads data, and executes the MLFlow pipeline for training,
    evaluating, and saving the machine learning model.
    """
    try:
        #create logger
        logger_save_ID=MODULE_NAME
        logger_name=MODULE_NAME
        logger=get_logger(logger_save_ID, logger_name, LOGGER_LEVEL)
    
        # Load training configuration
        config = load_train_config(logger,CONFIG_PATH)
        if config['csv_or_sql'] =='sql':
            train, test = load_data_sql(config['sql_query_train'],
                                        config['sql_query_test'],
                                        config['sql_connection_url'],logger)
        else:
             train, test = load_data_csv(config['train_path'], config['test_path'], logger)
   
         # Execute MLFlow pipeline: trains, evaluate and save the model
        train_evaluate_mlflow(EXPERIMENT_NAME,RUN_NAME,train,test, logger,RANDOM_SEED, MODEL_NAME, 
                              TAGS,MLFLOW_TRACKING_URI)
        
    except Exception as e:
        logger.error(f"An error occurred during pipeline execution: {e}")
        raise

if __name__ == "__main__":
    main()
