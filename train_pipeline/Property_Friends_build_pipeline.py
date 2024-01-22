"""
Module for building the machine learning model pipeline for property price prediction.

The pipeline is based on a Gradient Boosting Regressor and includes preprocessing steps for both categorical
and numerical data. The script utilizes scikit-learn's pipeline feature to streamline the process of transforming
data and applying the model. It includes data transformation and imputation steps.

Target encoding is used for categorical data, while numerical data is standardized. The function also produces a
dict to integrate with MLFlow for logging the preprocessing steps and model parameters, aiding in experiment
tracking and reproducibility.

Custom functions from the 'Property_Friends_prepare_data' module are used for data preparation, 
making this script part of a larger data analysis and machine learning project focused on 
property price prediction.
"""

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from category_encoders import TargetEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


#custom import
from Property_Friends_prepare_data import get_columns_type




def build_pipeline(logger,random_seed=42):  
    """
    Build a machine learning pipeline for property price prediction.

    This function creates a pipeline that includes preprocessing (imputation, encoding and standardization) 
    and a Gradient Boosting Regressor model. The function also logs the preprocessing steps and model parameters.

    Parameters:

    logger (Logger): The logger object for logging information.
    random_seed (int, optional): The random seed for reproducibility. Defaults to 42.

    Returns:

    tuple: A tuple containing the pipeline object and a dictionary of pipeline parameters.

    Raises:
    
    Exception: An exception is raised and logged if any unexpected error occurs during the model building process.
    """
    
    categorical_cols, numerical_cols, _ = get_columns_type()
    
    try:
        
        #data transformation
        categorical_transformer = TargetEncoder()
        #added standardscaler transformer
        standard_transformer = StandardScaler()
        
        #Simple techniques to deal with missing data
        categorical_imputer = SimpleImputer(strategy='most_frequent')
        numerical_imputer = SimpleImputer(strategy='mean')
        preprocessor = ColumnTransformer(transformers=[
            #preprocessing on categorical columns
            ('categorical_preprocess', Pipeline([
                ('input_missing_cat', categorical_imputer),
                ('categorical_encoder', categorical_transformer)
                ]), categorical_cols),
            #preprocessing on numerical columns 
            ('numerical_preprocess', Pipeline([
                ('input_missing_num',numerical_imputer),
                ('standard scaler', standard_transformer)
                ]), numerical_cols)
        ])
        #specify with preprocessing steps were done for MLFlow registry
        #this just affect the log and not the training
        data_log_params={
        'preprocess1':'cat_input_missing' ,   
        'preprocess2':'cat_encoder',
        'preprocess3':'num_input_missing',
        'preprocess4':'standard scaler'
        }
   
    
        #model config
        model_params = {
            'learning_rate': 0.01,
            'n_estimators': 300,
            'max_depth': 5,
            'loss': "absolute_error",
            'random_state':random_seed
        }
    
        steps = [
            ('preprocessor', preprocessor),
            ('model', GradientBoostingRegressor(**model_params))
        ]
        pipeline = Pipeline(steps)

        # Combine data_log_params and model_params
        # shows this data on MLFlow logs
        pipeline_params = {**model_params,**data_log_params,}
        
        return(pipeline, pipeline_params)
        
    except Exception as e:
        logger.error(f"Unexpected error during model building: {e}")
        raise
