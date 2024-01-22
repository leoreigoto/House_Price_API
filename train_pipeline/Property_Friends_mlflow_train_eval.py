"""
This module contains the functionality for training and evaluating machine learning models for property price
prediction. It uses MLflow for experiment tracking and logging, enabling the analysis of model performance and
parameter tuning over various runs. The module integrates several steps including data preparation, model 
building, training, evaluation, and logging.

The module is designed to work with specific custom modules like Property_Friends_model_evaluate, 
Property_Friends_prepare_data, and Property_Friends_build_model, which need to be available in the working
environment.
"""


import mlflow

#this import exists on the default file, but isn't used.
#Consider testing GridSearchCV for hyperparameter calibration
#from sklearn.model_selection import GridSearchCV

#custom import
from Property_Friends_model_evaluate import evaluate_model
from Property_Friends_prepare_data import get_columns_type, get_input_output
from Property_Friends_build_pipeline import build_pipeline



       
#Train with mlflow and saving in a sqlite DB
#run on cmd: mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host <HOST ADRESS> --port <PORT>

def train_evaluate_mlflow(exp_name, run_name, train_data, validate_data, logger, random_seed=42, 
                          model_name='model', tags={"tag1":"House Price Prediction" ,"tag2":"GradientBoostingRegressor"}, 
                        mlflow_tracking_uri='http://127.0.0.1:5000'):

    """
    Train and evaluate a machine learning model using MLflow, and log the process in an MLflow server.

    This function prepares the data, builds a machine learning pipeline, trains the model on the training data,
    evaluates it using the validation data, and logs the training parameters, metrics, and model in MLflow.

    Train and evaluate a machine learning model, and log the results using MLflow.

    Parameters:
 
     exp_name (str): Name of the MLflow experiment.
     run_name (str): Name of the MLflow run.
     train_data (DataFrame): Training data.
     validate_data (DataFrame): Validation data.
     logger (Logger): Logger for logging messages.
     random_seed (str, optional): The random seed for reproducibility. Defaults to 42.
     model_name (str, optional): Name of the model to log in MLflow. Defaults to 'model'.
     tags (dict, optional): Tags to set for the MLflow run. Defaults to {"tag1": "House Price Prediction",
                            "tag2": "GradientBoostingRegressor"}.
     mlflow_tracking_uri (str, optional): URI of the MLflow tracking server. Defaults to 'http://127.0.0.1:5000'.

    Raises:
 
     Exception: If any error occurs during the training or logging process.
    """
    

    #prepare data and build model
    X_train, y_train= get_input_output(train_data,logger)
    X_val, y_val = get_input_output(validate_data,logger)
    pipeline, pipeline_params = build_pipeline(logger,random_seed)
 
        
    try:
        mlflow.set_tracking_uri(mlflow_tracking_uri) 
        mlflow.set_experiment(exp_name)
        
    except Exception as e:
        logger.error(f"Problem loading mlflow experiment and tracking uri: {e}")
        raise 
    

    try:
        with mlflow.start_run(run_name= run_name ):
                    
            pipeline.fit(X_train,y_train)
            
            #log training parameters
            for parameter in pipeline_params:
                mlflow.log_param(parameter, pipeline_params[parameter])
            
            
            metrics_dict = evaluate_model(pipeline,X_val,y_val,logger,getdict=True)
            
            #log training metrics
            for metric in metrics_dict:
                mlflow.log_metric(metric, metrics_dict[metric])
                

            #set model tags
            mlflow.set_tags(tags)

            mlflow.sklearn.log_model(pipeline, model_name) 
                        

    except Exception as e:
        logger.error(f"Unexpected error during model training: {e}")
        raise            

