"""
Configuration Loader Module for Machine Learning Applications.

This module contains functions for loading and validating configuration settings 
from JSON files for a machine learning application, specifically 
focusing on training phase. It ensures that all necessary configuration 
parameters are present, either by reading them from a file or by setting them to 
default values if they are missing or in case of errors during file loading.

Function:
- load_train_config: Loads and validates the training configuration.
  Reads a configuration file, checks for required fields, and fills in any missing 
  fields with default values. It handles file not found, invalid JSON format, and other unexpected 
  errors by returning default configurations.
  Default configuration doesn't apply for SQL fields: url and query.

Exception handling and logging are integral parts of the module, ensuring that any issues with 
configuration files are clearly reported and gracefully handled.

SQL query and URL dont have a default value, in case they are missing
the code will get an error.
When database is ready, consider adding default values.
"""


import json

    

def load_train_config(logger,config_path='config.json'):
    """
    Load training-specific configuration settings from a JSON file.

    This function defines the required fields and default values for training configuration, 
    and then load these settings from the specified file.

    Parameters:
    - logger (Logger): Logger object for logging messages.
    - config_path (str, optional): Path to the configuration file. Defaults to 'config.json'.

    Returns:
    - dict: A dictionary containing the training configuration settings.
    
    SQL query and URL dont have a default value, in case they are missing
    the code will get an error.
    When database is ready, consider adding default values.
    """
    
    logger.info(f"Loading {config_path}")
    default_values={'csv_or_sql':'csv',
                    'train_path': 'data/train.csv',
                    'test_path': 'data/test.csv',
                    'sql_query_train':'',
                    'sql_query_test':'',
                    'sql_connection_url':''
                }
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
            
            #check for csv or sql field
            try:
                csv_sql=config['csv_or_sql']     
            except:
                logger.warning(f"Warning:'csv_or_sql' is missing in the config file. \
                               Setting to csv")
                csv_sql='csv'
            
    
            if csv_sql == 'sql' :
                required_fields = ['sql_query_train','sql_query_test','sql_connection_url']
                    
            else:   
                if csv_sql !='csv':
                    logger.warning(f"Warning: Invalid value for csv_or_sql. Changing to csv")
                    csv_sql='csv'
                    
                required_fields = ['train_path', 'test_path']
                default_values = {
                    'train_path': 'data/train.csv',
                    'test_path': 'data/test.csv',
                }
                
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
        logger.error(f"Unexpected error loading config: {e}. Returning default config.")
    return default_values