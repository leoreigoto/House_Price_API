"""
This script defines a function to evaluate a machine learning model using a set of validation data. 
The function, evaluate_model, takes a scikit-learn pipeline object and validation data as inputs 
and computes key performance metrics: Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE),
and Mean Absolute Error (MAE). 

The function is designed to work with any model that follows the  scikit-learn pipeline structure,
making it versatile for various regression tasks.

The flexibility to return metrics either as a tuple or as a dictionary
(controlled by the getdict parameter) allows  for easy integration of this function into
larger data analysis workflows or interactive analysis sessions.
"""

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, mean_absolute_error

def evaluate_model(pipeline,X_val,y_val,logger,getdict=False):  
    """
    Evaluate the given pipeline on the validation data.

    Parameters:
    pipeline (Pipeline): The pipeline to evaluate.
    X_val: Features of the validation dataset.
    y_val: Target values of the validation dataset.
    logger (Logger): Logger for logging information.
    getdict (bool): If True, return the evaluation metrics as a dictionary.

    Returns:
    tuple or dict: RMSE, MAPE, and MAE metrics as a tuple if getdict is False, else a dictionary.
    
    Raises:
    Exception: If an error occurs during prediction or evaluation.
    """
    

    try:
        predictions = pipeline.predict(X_val)
    except Exception as e:
        logger.error(f"Error during model prediction: {e}")
        raise 
   
    rmse = np.sqrt(mean_squared_error(predictions, y_val))
    mape = mean_absolute_percentage_error(predictions, y_val)
    mae = mean_absolute_error(predictions, y_val)

    #print(f"RMSE: {rmse}")
    #print(f"MAPE: {mape}")
    #print(f"MAE : {mae}")
    metrics_log={
        "RMSE": rmse,
        "MAPE": mape,
        "MAE" : mae
        }
           
    logger.info(f"RMSE: {rmse} | MAPE {mape} | MAE {mae}")
    
    if getdict:
        return metrics_log
  
    return rmse, mape, mae
