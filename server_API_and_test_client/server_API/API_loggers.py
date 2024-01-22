"""
This module provides the functionality to create and configure specialized loggers for different 
aspects of an API module within a house price prediction application.

The primary function `get_api_loggers` sets up three distinct loggers: one for general logging 
(generic_logger), one for monitoring input anomalies (input_logger), and one for logging prediction 
histories (pred_logger). These loggers facilitate detailed and categorized logging, aiding in 
effective monitoring and debugging.

Functions:
    get_api_loggers: Initializes and configures three distinct loggers for various logging needs 
                     within the API module.
"""

import logging

#custom imports
from create_logger import get_logger

    
    
def get_api_loggers(module_name):
    """
    Create and configure loggers for different aspects of an API module.

    This function initializes three distinct loggers for general information, input anomalies, 
    and prediction history, respectively. Each logger is configured with a unique identifier 
    and name based on the provided module name. The loggers are intended for different logging 
    purposes within the API module.

    Args:
        module_name (str): The name of the module for which loggers are being created. This name is 
                           used as part of the logger's identifier and name.

    Returns:
        tuple: A tuple containing three loggers: generic_logger, input_logger, and pred_logger.

    Raises:
        RuntimeError: If there is an error in creating any of the loggers, a RuntimeError is raised 
        with the error message.
    """
    try:
        # Generic logger for general information
        generic_logger_save_ID=module_name
        generic_logger_name=module_name
        generic_logger_level=logging.INFO
        generic_logger = get_logger(generic_logger_save_ID,generic_logger_name,generic_logger_level)

        # Logger for monitoring input anomalies
        input_logger_save_ID=f"{module_name}_input_anomaly"
        input_logger_name=f"{module_name}_input_anomaly"
        input_logger_level=logging.INFO
        input_logger = get_logger(input_logger_save_ID,input_logger_name,input_logger_level)

        # Logger for prediction history (conditional on enable_pred_data_log)
        pred_logger_save_ID=f"{module_name}_preds_history"
        pred_logger_name=f"{module_name}_preds_history"
        pred_logger_level=logging.INFO
        pred_logger = get_logger(pred_logger_save_ID,pred_logger_name,pred_logger_level)
        
    except Exception as e:
        # Handle any exception that occurs during logger creation
        raise RuntimeError(f"Error creating loggers for module {module_name}: {e}")
    
    return(generic_logger,input_logger,pred_logger)
