"""
This module provides functionality for loading machine learning models either from a local file system or via
MLflow. It supports loading models saved with joblib and updating the model configuration as necessary. 
The module is designed to be integrated into machine learning pipelines or applications that require dynamic 
model loading and updating based on different versioning systems.

Functions:
    load_local_model(model_path, generic_logger): Loads a model from a local file path using joblib.
    load_mlflow_model(mlflow_model_version, config, config_path, generic_logger): Loads a model via MLflow,
   updates the local configuration, and saves the model locally.
"""
from pathlib import Path
from joblib import load, dump
import mlflow
import json

def load_local_model(model_path,generic_logger):
    """
    Loads a machine learning model from a specified local file path using joblib. If the model file is not 
    found or any other error occurs, an appropriate log message is recorded, and the exception is raised.
    
    Parameters:
        model_path (str): The path to the model file to be loaded.
        generic_logger (logging.Logger): The logger object for logging messages during the model loading process.

    Returns:
        object: The loaded model object.

    Raises:
        FileNotFoundError: If the model file is not found at the specified path.
        Exception: For any other errors encountered during model loading.
    """
    
    try:
        model = load(Path(model_path))
        generic_logger.info("Local model loaded")
        return model
        
    except FileNotFoundError:
        generic_logger.critical(f"Model file not found at: {model_path}")
        raise
    
    except Exception as e:
        generic_logger.critical(f"Error loading local model: {e}")
        raise e
    


def load_mlflow_model(mlflow_model_version, config, config_path, generic_logger):
    """
    Loads a machine learning model from MLflow using a specified version, updates the local configuration
    file with the new model version, and saves the model locally using joblib. It handles exceptions during
    the loading process and logs appropriate messages.

    Parameters:
        mlflow_model_version (str): The version of the model to load from MLflow.
        config (dict): A dictionary containing the current configuration settings.
        config_path (str): The path to the configuration file to be updated.
        generic_logger (logging.Logger): The logger object for logging messages during the model loading process.

    Returns:
        tuple: A tuple containing three elements:
               1. success (bool): True if the model is successfully loaded and saved; otherwise False.
               2. model (object or None): The loaded model object, or None if loading failed.
               3. model_version (str or None): The version of the loaded model, or None if loading failed.

    Raises:
        Exception: For any errors encountered during model loading from MLflow.
    """
    
    sucess = False
    try:
        model_uri = f"models:/{config['model_name']}/{mlflow_model_version}"
        model = mlflow.sklearn.load_model(model_uri)
        model_version = mlflow_model_version

        #save the model using joblib
        save_path=config['models_path']
        save_filename=config['model_file_name']
        Path(save_path).mkdir(parents=True, exist_ok=True)
        save_model_path = Path(save_path) / save_filename
        dump(model, save_model_path)
        
        # Update the model_version in config file
        config['model_version'] = mlflow_model_version
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=4)
        
        
        
        generic_logger.info("Model sucefully updated")   
        sucess=True
        
        return sucess, model, model_version
        
    except Exception as e:
        generic_logger.error(f"Error loading MLFLOW serving model: {e}")
        return sucess, None, None