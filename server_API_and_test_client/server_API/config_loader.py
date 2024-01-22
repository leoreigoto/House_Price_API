"""
Configuration Loader Module for the house price prediction API.

This module contains functions for loading and validating configuration settings 
from JSON files for a machine learning application, specifically 
focusing on prediction phase. It ensures that all necessary configuration 
parameters are present, either by reading them from a file or by setting them to 
default values if they are missing or in case of errors during file loading.

Function:
- load_predict_config: Loads and validates the training configuration.
  Reads a configuration file, checks for required fields, and fills in any missing 
  fields with default values. It handles file not found, invalid JSON format, and other unexpected 
  errors by returning default configurations.
  Default configuration doesn't apply for SQL fields: url and query.

Exception handling and logging are integral parts of the module, ensuring that any issues with 
configuration files are clearly reported and gracefully handled.
"""

import json


def load_predict_config(logger,config_path='config.json'):
    """
    Load prediction-specific configuration settings from a JSON file.

    This function defines the required fields and default values for prediction configuration, 
    and then load these settings from the specified file.If any required fields are missing in the configuration
    file, this function sets them to default values and logs a warning.
    
    The function handles file not found errors, invalid JSON format errors, and other unexpected exceptions 
    by logging appropriate error messages and returning default configuration values.

    Parameters:
    - logger (Logger): Logger object for logging messages.
    - config_path (str, optional): Path to the configuration file. Defaults to 'config.json'.

    Returns:
    - dict: A dictionary containing the prediction configuration settings.
    
    Raises:
        FileNotFoundError: If the configuration file is not found.
        json.JSONDecodeError: If the configuration file is not a valid JSON file.
        Exception: For any other unexpected errors encountered during loading.
    """
        
    logger.info(f"Loading {config_path}")
    
    required_fields = ['model_name','model_alias', 'models_path', 'model_file_name', 'model_version',
                       'enable_pred_data_log','model_update_timer','health_check_timer']
    default_values = {
        'model_name': 'House_Price',
        'model_alias': 'production',
        'model_version': '1',
        'models_path': 'models',
        'model_file_name': 'local_model.pkl',
        'enable_pred_data_log': True,
        'model_update_timer': 60,   # in seconds
        'health_check_timer': 60     # in seconds
    }
    
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
            missing_fields = [field for field in required_fields if field not in config]
            if missing_fields:
                logger.warning(f"Warning: The following required fields are missing in the \
                               config file: {', '.join(missing_fields)}")
                logger.warning("Setting these fields to default values")
                for field in missing_fields:
                    config[field] = default_values[field]
        return config
    except FileNotFoundError:
        logger.error(f"Error: {config_path} not found. Returning default config.")
    except json.JSONDecodeError:
        logger.error(f"Error: {config_path} is not a valid JSON file. Returning default config.")
    except Exception as e:
        logger.error(f"Unexpected error loading config: {e}")
    return default_values
