import pandas as pd
from sqlalchemy import create_engine

def load_data_csv(train_path, test_path, logger):
    """
    Load training and testing data from CSV files.

    Parameters:
    - train_path (str): Path to the training data CSV file.
    - test_path (str): Path to the testing data CSV file.
    - logger (Logger): Logger object for logging messages.

    Returns:
    tuple: A tuple containing two pandas DataFrames, (train, test).

    Raises:
    Exception: Propagates any exception raised during data loading.
    """
    try:
        train = pd.read_csv(train_path)
        test = pd.read_csv(test_path)
        return train, test
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise
 
def load_data_sql(query_train, query_test, connection_url, logger):
    """
    Load data from a database using SQLAlchemy.

    query_train (str): SQL query for fetching the training data.
    query_test (str): SQL query for fetching the test data.
    connection_url (str): Connection URL to the SQL database.
    logger (Logger): Logger for logging error messages.

    Returns:
    pd.DataFrame: Data loaded from the database.
    
    Raises:
    Exception: Propagates any exception raised during data loading.
    """
    try:
        # Create an engine that connects to the specified database
        engine = create_engine(connection_url)

        # Execute the query and load data into a DataFrame
        with engine.connect() as connection:
            train = pd.read_sql(query_train, connection)
            test  = pd.read_sql(query_test, connection)

        return train,test

    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise
 
