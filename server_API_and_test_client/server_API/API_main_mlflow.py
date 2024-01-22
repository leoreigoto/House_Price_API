"""
This module integrates FastAPI with MLflow to serve a machine learning model for predicting
house prices. The API provides endpoints for retrieving model information, performing predictions, 
and checking server health. The module incorporates background tasks for updating the model and monitoring 
server status. The model is updated when another version receives the production alias in the mlflow server.
When the model is updated a local copy is saved on the server side.

Key Components:
- FastAPI application setup with route handlers for '/info', '/predict', and '/health' endpoints.
- Asynchronous tasks for checking model updates and server health.
- Configuration management and logging setup.
- Security measures through API key validation.

Usage:
The application should be run with a suitable ASGI server like Uvicorn or Hypercorn. Configuration
parameters like model file path should be set up in the 'config.json' file.
"""

from fastapi import FastAPI, HTTPException, Depends
from pathlib import Path
import pandas as pd
from typing import List
import asyncio
import mlflow

#custom imports
from API_loggers import get_api_loggers
from config_loader import load_predict_config
from API_class_models_metrics import InputData, StandardResponse, get_predict_log, monitor_input_metrics
from API_security_key import validate_api_key
from API_model_loader import load_local_model, load_mlflow_model


MODULE_NAME = 'API_House_mlflow'
CONFIG_PATH= 'config.json'

#Configure MLflow to connect to your server (its configurated in the training pipeline docker)
#you need to connect MLFlow with sqlite database before hand
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow_client = mlflow.tracking.MlflowClient()

#generic_logger -> general logging 
#input_logger -> input anomalies logging
#pred_logger -> prediction history logging. Only works if its enabled on config file.  
generic_logger,input_logger,pred_logger=get_api_loggers(MODULE_NAME)

config=load_predict_config(generic_logger,config_path=CONFIG_PATH)
model_name=config['model_name']
model_alias= config['model_alias']
model_version=config['model_version']
model_update_timer=config['model_update_timer']
model_path=config['models_path']
model_file_name=config['model_file_name']
enable_pred_data_log=config['enable_pred_data_log']
health_check_timer=config['health_check_timer']

model = None
load_model_path = Path(model_path) / model_file_name
app = FastAPI(title = model_name)


#Background tasks
async def check_model_update():
    """
    Asynchronously checks for updates to the MLflow model at regular intervals specified by 'model_update_timer'.
    If a new version is found, it loads the updated model, configures it for use and save a local copy.

    This function is intended to be run as a background task in the FastAPI app.
    """
    global model, model_version
    
    while True:
        try:
            await asyncio.sleep(model_update_timer)  # Check every "model_update_timer" seconds
            generic_logger.info("Checking if the model file has been updated...")
            mlflow_model_version = mlflow_client.get_model_version_by_alias(model_name,model_alias).version
            
            if mlflow_model_version != model_version:
                generic_logger.info(f"New version: changing local model to version {mlflow_model_version}")
                #loads model and update config file
                sucess, newModel,newVersion =load_mlflow_model(
                    mlflow_model_version, config, CONFIG_PATH, generic_logger
                    )

                if sucess:
                    model = newModel
                    model_version = newVersion
            else:
                generic_logger.info("No new model update found. Continuing with the current model.")
                
        except Exception as e:
            # Log any errors that occur during the update check
            generic_logger.error(f"Error during model update check: {e}")
    

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
    
 
#Startup tasks
async def startup_event():
    """
    Startup event handler for the FastAPI app. It checks and loads the appropriate MLflow model version at app startup.
    Also, initializes background tasks for model update checks and server status monitoring.

    Raises:
        Exception: If loading the model fails.
    """
    
    global model
    # Load the model when the application starts
    generic_logger.info("Checking if the model file has been updated...")
    try:
        mlflow_model_version = mlflow_client.get_model_version_by_alias(model_name,model_alias).version
        if mlflow_model_version != model_version:
            generic_logger.info(f"New version: changing local model to version {mlflow_model_version}")
            load_mlflow_model(mlflow_model_version, config, CONFIG_PATH, generic_logger)
        else:
            generic_logger.info("No new model update found. Continuing with the current model.")
            try:
                model = load_local_model(load_model_path, generic_logger)

            except:
                generic_logger.info("Error getting local model. Getting MLFlow model...")
                try: 
                    _, newModel, _ =load_mlflow_model(mlflow_model_version, config, CONFIG_PATH, generic_logger)
                    model = newModel

                except Exception as e:
                    generic_logger.critical(f"Failed to load local and mlflow model: {e}")
                    raise e
 
    except Exception as e:  
            generic_logger.error(f"Error during model update check: {e}")   
            raise e

    # Start the background tasks
    asyncio.create_task(check_model_update())
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
