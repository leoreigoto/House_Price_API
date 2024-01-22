# House Price prediction: API and automated pipeline to train and serve the model to the API

This repository contains the code for a FastAPI-based application designed for predicting house prices. It integrates FastAPI with MLflow, offering endpoints for model information retrieval, predictions, and health checks. 

## This code consists of two parts:

- House_API: API on fastapi to predict house price of the inputs. The API also got a toy model of a client generating requests to the API

- 'Property_Friends' machine learning pipeline: An automated pipeline to load data, process data, train, evaluate, log the model artificats using mlflow and  manage which model will be served to the House_API.

Both applications got a docker image, are easily scalable and adheres good programming pratices including modularization and documentation (which docstrings on the files).
They are also hightly customizable because of their modular components and also got a config.json file where a user can easily change some configurations. 
Ie: for the training pipeline a user can specify to feed data with csv files or SQL connection.


## This Readme includes:
- Changes from the notebook code and new pipeline (to ensure data robustness)
- How to run the API and train pipeline
- How to customize some parameters
- House_API: modules description (from modules docstrings) and function descriptions (from functions docstrings)
- Training_pipeline: modules description (from modules docstrings) and function descriptions (from functions docstrings)
- Possible improvements

## Changes in the original notebook code

The notebook had data leak, the column price was inside the input data. It was removed.

Included new pipelines to include robustness to the model:

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/2668e6b4-f3c3-4573-965f-24723abccb16)




## Running the code

Test if the mlflow is working:

run on cmd: "mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 127.0.0.1 --port 5000"
inside of training_pipeline folder

run on cmd: "mlflow ui" and check if its working

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/5a5b81b0-6119-414c-ae34-56ddeeb9a63c)

Proceed to install docker containers:

Go to train_pipeline folder and run on cmd:

"docker build . -t house_price_api_ml_pipeline_v1"

Then go to server_API folder and run on cmd:

"docker build . -t house_price_api_server_v1"

Open docker desktop:

Click on 'house_price_api_ml_pipeline_v1" image, then click on the button to start it :

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/f1a7ef3e-a783-4fce-b0ce-663c37d150a7)

Fill the informations bellow and click on run:

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/37da1742-abdf-4533-87ed-022563cf09e3)

Now run the image "house_price_api_server_v1" image and fill the information bellow:

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/16835969-aab0-479b-b3f0-931ce36fed12)



The application wont start. You need to change the mlflow IP adress for the container adress in the docker network.

Go to Container -> house_API_container -> Files -> HouseAPI and right click to edit API_main_mlflow.py

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/368f1f3c-c278-48ab-a8ad-f55aee2a8dfc)


On cmd run: 

"docker inspect House_ML_Container"

Search for the IP adress. Keep this e-mail adress.

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/d6a2b96e-b548-4516-84a5-803051408452)


Replace the adress in line 39 of API_main_mlflow.py to the one you found:

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/372d4e5b-9424-4583-9b99-cbf2ee60d0c8)

Click on save and restart container

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/354cd609-b15d-438c-9bd3-a5472628fb9c)


The application should start now:

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/178a49a0-e10d-4aa9-879f-f4c1f9d56a66)


Troubleshoot: If you get an error after last step, your port might be in use. Try to assign host port as 0 and docker will try to find an open port.

------

## Hosting API on docker and testing edge cases

(check the toy client inside server_API folder for mora details)

![](https://github.com/leoreigoto/House_Price_API/blob/main/ezgif-4-64749a6e8b.gif)


------

## Training the model with mlflow and deploying it on the API

1. On ML Pipeline container go to "Exec" and run "python Property_Friends_main.py"

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/bfbc3249-dccd-425d-a3a4-403ca227e4a6)

2. A new experiment should appear om mlflow ui  (http://127.0.0.1:5000/)

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/3fb1d87d-a22b-44c0-bede-50570e1ca190)

3. Click on the run. There you can check model config in "parameters" or metrics in "metrics".

4. To register the model click on deploy and them select the model name

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/f46477a6-2e09-4f26-9abc-4c9e20cc3ea3)

5. You can check registered models on "models" page

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/4da281ef-5b69-48ce-bd76-c5f5a203cde3)

6. Clicking in the model name you can also set an alias for it

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/bb2dac5c-b84f-4edd-a4a3-856ade1a9b5f)

7. The fastapi will load whatever model matches the name and alias in the server config.json file

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/18858156-fbca-4864-8565-4f7745edb7e3)

------

## Training a model with different parameters or different preprocessing steps

1. Change parameters in Property_Friends_build_pipeline.py:

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/8911771b-59d3-4aa7-8774-46dd1b53d9f1)

2. train the model

3. check results on mlflow API and compare results:

previous experiment:

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/681cffd0-7555-4e70-a256-21352ca9c595)

new experiment:

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/a81bda13-c2f1-40d2-a930-706daf1277d4)


## Adding new inputs to the model:

1. Open Property_Friends_prepare_data.py:

2. Insert column name under "categorical_cols" or "numerical_cols" in get_columns_type()

![image](https://github.com/leoreigoto/House_Price_API/assets/48571786/c501f1d3-83b8-4de0-8b72-b39311416b22)

## Changing training data from csv to SQL

1. Open config.json
   
2. Change "csv_or_sql" to "sql" and change "sql_query_train", "sql_query_test" and "sql_connection_url"
 
------

## House_API

### API Files: general overview

-API_main_mlflow: main file of the API, used to start it. This version got integration with mlflow  to manage production model (need to insert 'production' tag on mlflow registred model). Dependency: running the command to connect mlfLow with a sqlite database in the training pipeline. 

-API_main_standalone: alternative option to the main file, this one doesn't integrate with mlflow and only run local models. Its ommited from the modules descritipn because of the similarity of APIN_main_mlflow, but the file contains the docstrings for the module and functions.

-API_model_loader: module with functions to load model (locally and from mlflow)

-API_class_models_metrics: module with Pydantic BaseModels and functions to log metrics

-API_security_key: module to generate a security key and validate it on endpoints.

-API_loggers: module to generate loggers of the API (general logger, input anomaly monitor logger and prediction history logger - prediction history can be disabled)

-create_logger (also included in the ML pipeline): module to create generic loggers)

-config_loader: module to load default config from a .json file and load default values in case of missing values

-config.json: config values of the API

-requirements.txt: requirements to run the API.

-keys/key_app.env: API security key

-models/local_model.pkl (temporary): local saved model (not needed if running API_main_mlflow) - API_main_mlflow will overwrite with a new version from mlflow if detected

-logs/: API_House_mlflow*/2024-01/*: some examples of loggers from API_main_mlflow

-logs/: API_House_standalone*/2024-01/*: some examples of loggers from API_main_standalone

-client_test/Test_API.ipynb: jupyter notebook simulating a client generating requests from the API. Contain edge cases, one of them generates a error (missing required input field)

-client_test/client_key/client_keys.env: API acess key (for the client)

-Dockerfile: file to generate docker image.

-.dockerignore: ignore list of docker

------

# House API : modules and functions description (also included in files docstrings):

------

### API_main_mlflow.py:

This module integrates FastAPI with MLflow to serve a machine learning model for predicting house prices. The API provides endpoints for retrieving model information, performing predictions,  and checking server health. The module incorporates background tasks for updating the model and monitoring  server status. The model is updated when another version receives the production alias in the mlflow server. When the model is updated a local copy is saved on the server side.

Key Components:
- FastAPI application setup with route handlers for '/info', '/predict', and '/health' endpoints.
- Asynchronous tasks for checking model updates and server health.
- Configuration management and logging setup.
- Security measures through API key validation.

Usage:
The application should be run with a suitable ASGI server like Uvicorn or Hypercorn. Configuration
parameters like model file path should be set up in the 'config.json' file.

Functions:

async def check_model_update():

Asynchronously checks for updates to the MLflow model at regular intervals specified by 'model_update_timer'. If a new version is found, it loads the updated model, configures it for use and save a local copy.

This function is intended to be run as a background task in the FastAPI app.
    
async def check_server_status():

Asynchronously performs health checks on the server at regular intervals specified by 'health_check_timer'. Logs the status of the API server.

This function is intended to be run as a background task in the FastAPI app.

async def startup_event():

Startup event handler for the FastAPI app. It checks and loads the appropriate MLflow model version at app startup. Also, initializes background tasks for model update checks and server status monitoring.

Raises:
   
    Exception: If loading the model fails.

def model_predict(data: List[InputData]):

Performs prediction using the loaded ML model on the provided input data.

Args:

    data (List[InputData]): A list of InputData objects containing the features for prediction.

Returns:

    List: A list of predictions made by the model.

Raises:
   
    HTTPException: If an error occurs during the prediction process.

async def info(): 

Endpoint to get information about the current model in use, including its name, version, and alias. An API key is required to access this endpoint.
    
Returns:
   
    StandardResponse: Contains success status, endpoint information, and model details.

async def predict(data:List[InputData]):

Endpoint for predicting house prices based on the provided data. This endpoint calls model_predict function. An API key is required to access this endpoint.
    
Args:
    
    data (List[InputData]): A list of InputData objects containing the features for prediction.

Returns:
    
    StandardResponse: Contains success status, endpoint information, and prediction results.

Raises:
    
    HTTPException: If an error occurs during prediction or input metrics monitoring.

async def health():

Endpoint for checking the health and status of the API server. An API key is required to access this endpoint.
    
Returns:
   
    StandardResponse: Contains success status, endpoint information, and server health status.

------

### API_main_standalone.py:

Alternative to API_main_mlflow, but only uses a local model and doesn't connect with mlflow. This module and functions are documented with docstrings.

------

### API_model_loader.py:

This module provides functionality for loading machine learning models either from a local file system or via MLflow. It supports loading models saved with joblib and updating the model configuration as necessary. The module is designed to be integrated into machine learning pipelines or applications that require dynamic model loading and updating based on different versioning systems.

Functions:

def load_local_model(model_path,generic_logger):

Loads a machine learning model from a specified local file path using joblib. If the model file is not found or any other error occurs, an appropriate log message is recorded, and the exception is raised.
    
Parameters:
  
    model_path (str): The path to the model file to be loaded.
    generic_logger (logging.Logger): The logger object for logging messages during the model loading process.

Returns:
  
    object: The loaded model object.

Raises:
  
    FileNotFoundError: If the model file is not found at the specified path.
    Exception: For any other errors encountered during model loading.

def load_mlflow_model(mlflow_model_version, config, config_path, generic_logger):

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

------

### API_class_models_metrics.py:

This module defines the data models and logging functionalities for a house price prediction API.

It defines Pydantic models to structure and validate both the input and output data for house price predictions. The input data model supports optional fields, allowing flexibility in the data provided for predictions. The output data model is designed to structure the predicted price information. The module also includes functions for creating detailed logs of prediction requests and outputs, as well as monitoring input data for any anomalies.

The module is designed to be used in a house price prediction API, where reliable data validation, structured output, and detailed logging are crucial for maintaining data integrity, ensuring accurate predictions, and facilitating effective monitoring and debugging.

Classes:

class InputData(BaseModel):

Pydantic model for input data used in house price prediction, allowing for optional values.

This model defines the structure and data types for the input data required by the prediction model.
It supports optional fields, allowing for incomplete data entries. Fields not provided will be set to None.

    Attributes:
    type (str): The type of the property. Required.
    sector (Optional[str]): The sector in which the property is located. Can be omitted.
    net_usable_area (Optional[float]): The usable area of the property in square meters. Can be omitted.
    net_area (Optional[float]): The total area of the property in square meters. Can be omitted.
    n_rooms (Optional[float]): The number of rooms in the property. Can be omitted.
    n_bathroom (Optional[float]): The number of bathrooms in the property. Can be omitted.
    latitude (Optional[float]): The latitude of the property's location. Can be omitted.
    longitude (Optional[float]): The longitude of the property's location. Can be omitted.


StandardResponse (BaseModel): 

Defines the structure of a standard response for API endpoints.

This Pydantic model is used to standardize responses from various API endpoints, ensuring a consistent
structure across the API. It includes a success status, endpoint details, and an optional data field 
for additional information or results.

Attributes:

    success (bool): Indicates if the request was successful.
    endpoint (str): The name or path of the endpoint.
    data (dict, optional): Additional data or results from the endpoint. Default is None.


Functions:

def get_predict_log(input_data: List[InputData], output_data: dict,model_name, model_version,model_alias=None):

Create and return a JSON-formatted log entry for prediction requests and outputs.

This function pairs each input data item with its corresponding output prediction and includes details about the model used for the prediction. The result is formatted as a JSON string.

Args:

    input_data (List[InputData]): A list of input data instances.
    output_data (List[OutputData]): A list of output data instances corresponding to the input data.
    model_name (str): The name of the prediction model.
    model_version (str): The version of the prediction model.

Returns:
    
    str: A JSON-formatted string summarizing the prediction data and results.
    
def monitor_input_metrics(data: List[InputData], input_logger, generic_logger):

Monitor and log any anomalies found in the input data.

This function checks for invalid conditions in the input data, such as non-positive values for certain numeric fields. It aggregates all warnings and logs them in a single entry for efficiency.

Args:
        
    data (List[InputData]): A list of input data instances to be monitored.
    input_logger: The logger for recording input-specific logs.
    generic_logger: The logger for recording general logs.

Raises:

    Exception: If any error occurs during the monitoring process.

------

### API_security_key.py:

This module provides security features for a FastAPI application, specifically for API key validation. It includes the functionality to define an API key header, load API keys from environment variables, and validate the API key provided in the request headers against the expected key. The environment variables are loaded from a `.env` file, ensuring that sensitive information like API keys are not hard-coded into the application.

Functions:

async def validate_api_key(api_key: str = Depends(api_key_header)):

Validate the provided API key against the expected API key.

This function checks the API key provided in the request header. If the key matches the key stored in the environment variable, access is granted. Otherwise, an HTTP 403 Forbidden exception is raised, indicating invalid credentials.

Args:
    
    api_key (str): The API key retrieved from the request header.

Returns:
 
    bool: True if the API key is valid, otherwise raises HTTPException.

Raises:
    
    HTTPException: 403 error if the API key does not match

------

### API_loggers.py:

This module provides the functionality to create and configure specialized loggers for different aspects of an API module within a house price prediction application.

The primary function `get_api_loggers` sets up three distinct loggers: one for general logging (generic_logger), one for monitoring input anomalies (input_logger), and one for logging prediction histories (pred_logger). These loggers facilitate detailed and categorized logging, aiding in effective monitoring and debugging.

Functions:

def get_api_loggers(module_name):

Create and configure loggers for different aspects of an API module.

This function initializes three distinct loggers for general information, input anomalies, and prediction history, respectively. Each logger is configured with a unique identifier 
and name based on the provided module name. The loggers are intended for different logging purposes within the API module.

Args:
    
    module_name (str): The name of the module for which loggers are being created. This name is used as part of the logger's identifier and name.

Returns:
   
    tuple: A tuple containing three loggers: generic_logger, input_logger, and pred_logger.

Raises:

    RuntimeError: If there is an error in creating any of the loggers, a RuntimeError is raised with the error message.

------

### creater_logger.py (shared with training pipeline):

This module provides functionalities for setting up and configuring loggers with specific naming and directory structures. It allows for the creation of loggers with filenames that include a unique identifier and the current date, organized into directories based on the identifier and the current year and month. This is particularly useful for maintaining organized logging in applications where log separation based on time or specific identifiers is necessary.

Functions:

def get_logger(logger_save_ID,logger_name,level=logging.INFO):
Create and configure a logger with file handling.

This function sets up a logger to write logs to a file, organized by date and logger ID. The log directory and file are created if they don't exist. If the logger with the specified name already exists, it returns the existing logger without creating duplicate handlers.

Args:

    logger_save_ID (str): Identifier for the logger, used in naming log files.
    logger_name (str): Name of the logger.
    level (int, optional): Logging level. Defaults to logging.INFO.

Returns:

    logging.Logger: Configured logger with a file handler.

Raises:

    Exception: If there is an error in setting up the logger, an exception is raised with the error message.

------

### config_loader.py:

Configuration Loader Module for the house price prediction API.

This module contains functions for loading and validating configuration settings from JSON files for a machine learning application, specifically focusing on prediction phase. It ensures that all necessary configuration parameters are present, either by reading them from a file or by setting them to default values if they are missing or in case of errors during file loading.

Exception handling and logging are integral parts of the module, ensuring that any issues with configuration files are clearly reported and gracefully handled.

def load_predict_config(logger,config_path='config.json'):

Load prediction-specific configuration settings from a JSON file.

This function defines the required fields and default values for prediction configuration, and then load these settings from the specified file.If any required fields are missing in the configuration file, this function sets them to default values and logs a warning.
    
The function handles file not found errors, invalid JSON format errors, and other unexpected exceptions by logging appropriate error messages and returning default configuration values.

Parameters:

    logger (Logger): Logger object for logging messages.
    config_path (str, optional): Path to the configuration file. Defaults to 'config.json'.

Returns:

    dict: A dictionary containing the prediction configuration settings.
    
Raises:
    
    FileNotFoundError: If the configuration file is not found.
    json.JSONDecodeError: If the configuration file is not a valid JSON file.
    Exception: For any other unexpected errors encountered during loading

------

### config.json:

    {
    "model_name": "House_Price",
    "model_alias": "production",
    "model_version": "1",
    "models_path": "models",
    "model_file_name": "local_model.pkl",
    "enable_pred_data_log": true,
    "model_update_timer": 60,
    "health_check_timer": 60
    }

------

# Property Friends ML Pipeline

### ML Pipeline Files: general overview

- Property_Friends_main : main file that integrates the entire pipeline.
- Property_Friends_mlflow_train_eval: train the pipeline and integrates with mlflow for model tracking.
- Property_Friends_build_pipeline: build the preprocessing pipeline and the ML model.
- Property_Friends_model_evaluate: defines the function to evaluate the model.
- Property_Friends_prepare_data: defines the input data and describes if they are categorical or numerical data.
- Property_Friends_data_loader: load either csv or sql data.
- requirements.txt: requirements to run the ML pipeline.
- config_train_loader: load the train config data from a json file.
- config.json: config file.
- create_logger (shared with the API): create generical loggers.
- mlruns/*: artifcats generated from mlflow (including the trained model)
- mlflow.db: sqlite database used in mlflow
- logs/Property_Friends_main/20204-01/*: example logs generated by the ML Pipeline
- data: folder were the training and test data were located (excluded from the github/docker).


------

# ML Pipeline: modules and functions description (also included in files docstrings):

------

### Property_Friends_main.py

Main module for the 'Property_Friends' machine learning pipeline.

This module implements the main functionality for the Property Friends machine learning pipeline. It includes the integration of various components such as data loading, logging, configuration management, and the execution of the MLFlow pipeline for model training, evaluation, and saving. It integrates with MLflow for experiment tracking and model management.

The pipeline is specifically designed for the House Price Prediction use case, utilizing the Gradient Boosting Regressor algorithm. It leverages custom utility modules for configuration loading, logging, model evaluation, and MLFlow-based training and evaluation.

Constants:

    - MODULE_NAME: Name of the current module for logging purposes.
    - LOGGER_LEVEL: Logging level.
    - EXPERIMENT_NAME: Name of the MLFlow experiment.
    - MODEL_NAME: Name of the machine learning model.
    - TAGS: Tags for MLFlow logging.
    - RUN_NAME: Name of the MLFlow run
    - CONFIG_PATH: Path to load the config file
    - RANDOM_SEED: Fix a random seed to make the code reproducible

def main():

Main function to execute the machine learning pipeline.

This function initializes logging, loads configuration, reads data, and executes the MLFlow pipeline for training, evaluating, and saving the machine learning model.

------

### Property_Friends_mlflow_train_eval.py:

This module contains the functionality for training and evaluating machine learning models for property price prediction. It uses MLflow for experiment tracking and logging, enabling the analysis of model performance and parameter tuning over various runs. The module integrates several steps including data preparation, model building, training, evaluation, and logging.

The module is designed to work with specific custom modules like Property_Friends_model_evaluate, Property_Friends_prepare_data, and Property_Friends_build_model, which need to be available in the working environment.

def train_evaluate_mlflow(exp_name, run_name, train_data, validate_data, logger, random_seed=42, model_name='model', tags={"tag1":"House Price Prediction" , "tag2":"GradientBoostingRegressor"}, mlflow_tracking_uri='http://127.0.0.1:5000'):

Train and evaluate a machine learning model using MLflow, and log the process in an MLflow server.

This function prepares the data, builds a machine learning pipeline, trains the model on the training data, evaluates it using the validation data, and logs the training parameters, metrics, and model in MLflow.

Train and evaluate a machine learning model, and log the results using MLflow.

 Parameters:
 
     exp_name (str): Name of the MLflow experiment.
     run_name (str): Name of the MLflow run.
     train_data (DataFrame): Training data.
     validate_data (DataFrame): Validation data.
     logger (Logger): Logger for logging messages.
     random_seed (str, optional): The random seed for reproducibility. Defaults to 42.
     model_name (str, optional): Name of the model to log in MLflow. Defaults to 'model'.
     tags (dict, optional): Tags to set for the MLflow run. Defaults to {"tag1": "House Price Prediction", "tag2": "GradientBoostingRegressor"}.
     mlflow_tracking_uri (str, optional): URI of the MLflow tracking server. Defaults to 'http://127.0.0.1:5000'.

 Raises:
 
     Exception: If any error occurs during the training or logging process.
     
------

### Property_Friends_build_pipeline.py:

Module for building the machine learning model pipeline for property price prediction.

The pipeline is based on a Gradient Boosting Regressor and includes preprocessing steps for both categorical and numerical data. The script utilizes scikit-learn's pipeline feature to streamline the process of transforming data and applying the model. It includes data transformation and imputation steps.

Target encoding is used for categorical data, while numerical data is standardized. The function also produces a dict to integrate with MLFlow for logging the preprocessing steps and model parameters, aiding in experiment tracking and reproducibility.

Custom functions from the 'Property_Friends_prepare_data' module are used for data preparation, making this script part of a larger data analysis and machine learning project focused on property price prediction.

Functions:

def build_pipeline(logger,random_seed=42):  

Build a machine learning pipeline for property price prediction.

This function creates a pipeline that includes preprocessing (imputation, encoding and standardization) and a Gradient Boosting Regressor model. The function also logs the preprocessing steps and model parameters.

Parameters:

    logger (Logger): The logger object for logging information.
    random_seed (int, optional): The random seed for reproducibility. Defaults to 42.

Returns:

    tuple: A tuple containing the pipeline object and a dictionary of pipeline parameters.

Raises:
    
    Exception: An exception is raised and logged if any unexpected error occurs during the model building process.

------

### Property_Friends_model_evaluate.py:

This script defines a function to evaluate a machine learning model using a set of validation data. The function, evaluate_model, takes a scikit-learn pipeline object and validation data as inputs and computes key performance metrics: Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE), and Mean Absolute Error (MAE). 

The function is designed to work with any model that follows the  scikit-learn pipeline structure, making it versatile for various regression tasks.

The flexibility to return metrics either as a tuple or as a dictionary (controlled by the getdict parameter) allows  for easy integration of this function into larger data analysis workflows or interactive analysis sessions.


def evaluate_model(pipeline, X_val, y_val, logger, getdict=False):

Evaluate the given pipeline on the validation data.

This function predicts using the provided pipeline and validation data, then calculates and logs various evaluation metrics like RMSE, MAPE, and MAE. It can return these metrics either as separate values or as a dictionary.

Parameters:

    pipeline (Pipeline): The trained model pipeline.
    X_val (DataFrame): The input features of the validation dataset.
    y_val (Series): The target variable of the validation dataset.
    logger (Logger): Logger for logging evaluation results and errors.
    getdict (bool, optional): Flag to return metrics as a dictionary. Defaults to False.

Returns:

    tuple or dict: Evaluation metrics as separate values (RMSE, MAPE, MAE) or as a dictionary, depending on the 'getdict' flag.

Raises:

    Exception: If an error occurs during prediction or evaluation.

------

### Property_Friends_prepare_data.py:

This module provides a scalable way to change the inputs of the machine learning model with a small ammount of change in the code

def get_columns_type():

Define and return the column names for the machine learning model.

This function separates the column names into categorical, numerical, and target categories.
These categories are used in the preprocessing and modeling stages to apply appropriate 
transformations and to distinguish between features and the target variable.

Returns:

    tuple: A tuple containing three lists:
        - categorical_cols: List of names of categorical columns.
        - numerical_cols: List of names of numerical columns.
        - target: List containing the name of the target column.

def get_input_output(data,logger,input_only=False):

Extract input and output data from a given dataset based on predefined column types.

This function uses get_columns_type to determine the relevant columns for input (features) and output (target). It ensures that the dataset contains the expected columns and 
extracts them accordingly. The function can optionally return only the input data.

Parameters:

    data (DataFrame): The dataset from which to extract input and output data.
    logger (Logger): Logger object used for logging error messages.
    input_only (bool, optional): If True, the function returns only the input data. Defaults to False.

Returns:

    DataFrame or tuple of DataFrame: 
        - If input_only is False, returns a tuple containing two DataFrames (input_data, output_data).
        - If input_only is True, returns a single DataFrame (input_data).

Raises:

    KeyError: If a required column is not found in the dataset.
    ValueError: If there is a value-related error in processing the data.
    Exception: For any other unexpected errors encountered during data extraction

------

### Property_Friends_data_loader.py:

This module can load both csv (using pandas) or from a SQL database (using sqlalchemy)

def load_data_csv(train_path, test_path, logger)

Load training and testing data from CSV files.

Parameters:

    - train_path (str): Path to the training data CSV file.
    - test_path (str): Path to the testing data CSV file.
    - logger (Logger): Logger object for logging messages.

Returns:

    tuple: A tuple containing two pandas DataFrames, (train, test).

Raises:

    Exception: Propagates any exception raised during data loading.


def load_data_sql(query_train, query_test, connection_url, logger):

Load data from a database using SQLAlchemy.

Parameters:

    query_train (str): SQL query for fetching the training data.
    query_test (str): SQL query for fetching the test data.
    connection_url (str): Connection URL to the SQL database.
    logger (Logger): Logger for logging error messages.

Returns:

    pd.DataFrame: Data loaded from the database.
    
Raises:

    Exception: Propagates any exception raised during data loading.

------

###config_train_loader:

similar to the config_loader of the API. Just got a few changes on the required fields and default values.
SQL fields (url and query) dont have a default value.

------

### config.json:

    {
      "csv_or_sql": "csv",
      "train_path": "data/train.csv",
      "test_path": "data/test.csv",
      "sql_query_train": "",
      "sql_query_test": "",
      "sql_connection_url": ""
    }

------

###create_loggers.py:

same file used in the API.

------

Possible improvements:

- Add a data skew monitor and improve anomaly monitor logger. One fast solution could be using Alibi Detect

- Monitor and version input data. One solution could be using DVC

- Model parameters

- Integrate the API with a cloud service
