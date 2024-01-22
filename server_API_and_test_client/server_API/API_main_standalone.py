"""
This module integrates FastAPI with MLflow to serve a machine learning model for predicting
house prices. The API provides endpoints for retrieving model information, performing predictions, 
and checking server health. The module incorporates background task  monitoring server status. 

This is an alternative version of "API_main-mlflow" without the mlflow integration.

Key Components:
- FastAPI application setup with route handlers for '/info', '/predict', and '/health' endpoints.
- Asynchronous tasks for checking server health.
- Configuration management and logging setup.
- Security measures through API key validation.

Usage:
The application should be run with a suitable ASGI server like Uvicorn or Hypercorn. Configuration
parameters like model file path should be set up in the 'config.json' file.
"""
from fastapi import FastAPI, HTTPException, Depends
from joblib import load
from pathlib import Path
import pandas as pd
from typing import List
import asyncio

#custom imports
from API_loggers import get_api_loggers
from config_loader import load_predict_config
from API_class_models_metrics import InputData, StandardResponse, get_predict_log, monitor_input_metrics
from API_security_key import validate_api_key
from API_model_loader import load_local_model


MODULE_NAME = 'API_House_mlflow'
CONFIG_PATH= 'config.json'

       
#generic_logger -> general logging 
#input_logger -> input anomalies logging
#pred_logger -> prediction history logging. Only works if its enabled on config file. 
generic_logger,input_logger,pred_logger=get_api_loggers(MODULE_NAME)


config=load_predict_config(generic_logger,config_path=CONFIG_PATH)
model_name=config['model_name']
model_alias= config['model_alias']
model_version=config['model_version']
model_path=config['models_path']
model_file_name=config['model_file_name']
enable_pred_data_log=config['enable_pred_data_log']
health_check_timer=config['health_check_timer']

model = None
load_model_path = Path(model_path) / model_file_name



generic_logger.info('loading model')
load_local_model(load_model_path)
    
app = FastAPI(title = model_name)



async def check_server_status():
    """
    Asynchronously performs health checks on the server at regular intervals specified by 'health_check_timer'.
    Logs the status of the API server.

    This function is intended to be run as a background task in the FastAPI app.
    """
    while True:
         # Perform your health check logic here
        await asyncio.sleep(health_check_timer)  # Check every "health_check_timer" seconds
        generic_logger.info("Performing health check...")
        await health()
        
        
    
            
async def startup_event():
    """
    Handles the startup event for the FastAPI application.

    On startup starts the background task for checking server status.
    """
    
    asyncio.create_task(check_server_status())
    


# startup event handler -> activate start tasks
app.add_event_handler("startup", startup_event)


#general API functions

def model_predict(data: List[InputData]):
    """
    Performs prediction using the loaded ML model on the provided input data.

    Args:
        data (List[InputData]): A list of InputData objects containing the features for prediction.

    Returns:
        List: A list of predictions made by the model.

    Raises:
        HTTPException: If an error occurs during the prediction process.
    """
    try:
        model_inputs = pd.DataFrame([item.model_dump() for item in data])
        predictions = model.predict(model_inputs)
        generic_logger.info(f"Prediction completed.")
        return predictions.tolist()
    except Exception as e:
        generic_logger.error(f"Error during model prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Error during model prediction {e}") 
 
    

#API endpoints

@app.get('/info', summary="Get Model Information", response_model=StandardResponse, dependencies=[Depends(validate_api_key)])
async def info(): 
    """
    Endpoint to get information about the current model in use, including its name, version, and alias.
    An API key is required to access this endpoint.
    
    Returns:
        StandardResponse: Contains success status, endpoint information, and model details.
    """
        
    response_info = {}
    response_info["name"] = model_name
    response_info["version"] = model_version
    response_info["alias"] = model_alias
    
    return StandardResponse(success=True, endpoint="info", data=response_info)           
         
 

    
@app.post('/predict', response_model = StandardResponse,summary="Predict House Prices", dependencies=[Depends(validate_api_key)])
async def predict(data:List[InputData]):
    """
    Endpoint for predicting house prices based on the provided data. This endpoint calls model_predict function
    An API key is required to access this endpoint.
    
    Args:
        data (List[InputData]): A list of InputData objects containing the features for prediction.

    Returns:
        StandardResponse: Contains success status, endpoint information, and prediction results.

    Raises:
        HTTPException: If an error occurs during prediction or input metrics monitoring.
    """

    generic_logger.info(f"Received prediction request with input size: {len(data)}.")
    try:
        monitor_input_metrics(data, input_logger, generic_logger)
    except Exception as e:
        generic_logger.error(f"Error during metric monitor: {e}")
        raise HTTPException(status_code=500,detail=f"Error during metric monitor {e}")
    try:
        predictions=model_predict(data)
        if enable_pred_data_log:
            pred_logger.info(
                f"Prediction summary: {get_predict_log(data,predictions,model_name, model_version,model_alias)}"
            )
        return StandardResponse(success=True, endpoint="predict", data={'price':predictions})    
    
    except Exception as e:
        generic_logger.error(f"Error during model prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Error during model prediction {e}")
    

        
@app.get('/health',summary="Check Server Status",response_model=StandardResponse, dependencies=[Depends(validate_api_key)])
async def health():
    """
    Endpoint for checking the health and status of the API server.
    An API key is required to access this endpoint.

    Returns:
        StandardResponse: Contains success status, endpoint information, and server health status.
    """
 
    response_health={}
    response_health['API status']='online'
    generic_logger.info("Health check: API server online")
    return StandardResponse(success=True, endpoint="health", data=response_health)