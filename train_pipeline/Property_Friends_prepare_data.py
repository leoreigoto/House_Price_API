"""

Functions:
- get_columns_type: Defines and returns lists of categorical, numerical, and target column names.
- get_input_output: Extracts and returns input and output data from a dataset, ensuring 
  the data adheres to the expected structure and types.

This module provides a scalable way to change the inputs of the machine learning model with
a small ammount of change in the code
"""

def get_columns_type():
    """
    Define and return the column names for the machine learning model.

    This function separates the column names into categorical, numerical, and target categories.
    These categories are used in the preprocessing and modeling stages to apply appropriate 
    transformations and to distinguish between features and the target variable.

    Returns:
    tuple: A tuple containing three lists:
        - categorical_cols: List of names of categorical columns.
        - numerical_cols: List of names of numerical columns.
        - target: List containing the name of the target column.
    """
    
    #define model columns
    categorical_cols = ["type", "sector"]
    target = "price"
    #added numerical_cols, we didn't had any numerical transform (standardscaler, normalization, minmax, etc)  
    numerical_cols=['net_usable_area','net_area','n_rooms','n_bathroom','latitude','longitude']
    
    return categorical_cols, numerical_cols, target



def get_input_output(data,logger,input_only=False):
    """
    Extract input and output data from a given dataset based on predefined column types.

    This function uses `get_columns_type` to determine the relevant columns for input (features) 
    and output (target). It ensures that the dataset contains the expected columns and 
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
    Exception: For any other unexpected errors encountered during data extraction.
    """
    
    categorical_cols, numerical_cols, target = get_columns_type()
    
    #ensure that we don't have new columns inserted by accident
    input_columns = categorical_cols + numerical_cols
    
    try:
        input_data= data[input_columns]

        if input_only:
            return input_data
            
        output_data= data[target]
        
        return input_data, output_data
       
    except KeyError as e:
        logger.error(f"Error: Column not found in the dataset - {e}")
        raise
   
    except ValueError as e:
        logger.error(f"Error: Value error encountered - {e}")
        raise
   
    except Exception as e:
        logger.error(f"Unexpected error data preparing - {e}")
        raise