"""
This module defines the data models and logging functionalities for a house price prediction API.

It defines Pydantic models to structure and validate both the input and output data for house price predictions. 
The input data model supports optional fields, allowing flexibility in the data provided for predictions. 
The output data model is designed to structure the predicted price information. The module also includes 
functions for creating detailed logs of prediction requests and outputs, as well as monitoring input data 
for any anomalies.

Classes:
- InputData: A Pydantic model for input data validation. It includes both required and optional fields 
  to accommodate a variety of data entries for house price prediction.
- StandardResponse (BaseModel): Defines the structure of a standard API response including success status,
  endpoint, and dict response from specific endpoint.

Functions:
  get_predict_log(input_data: List[InputData], output_data: dict, model_name, model_version, model_alias):
  Converts prediction input and output data into a JSON formatted string for logging.
- monitor_input_metrics: Monitors the input data for anomalies (like non-positive values in numerical 
  fields) and logs warnings efficiently. It also handles exceptions during the monitoring process, logging 
  errors to both input-specific and general loggers.
  
The module is designed to be used in a house price prediction API, where reliable data validation, 
structured output, and detailed logging are crucial for maintaining data integrity, ensuring accurate 
predictions, and facilitating effective monitoring and debugging.
"""

from pydantic import BaseModel
from typing import List, Optional
import json

class InputData(BaseModel):
    """
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
    """

    type: str
    sector: Optional[str] = None
    net_usable_area: Optional[float] = None
    net_area: Optional[float] = None
    n_rooms: Optional[float] = None
    n_bathroom: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class StandardResponse(BaseModel):
    """
    Defines the structure of a standard response for API endpoints.

    This Pydantic model is used to standardize responses from various API endpoints, ensuring a consistent
    structure across the API. It includes a success status, endpoint details, and an optional data field 
    for additional information or results.

    Attributes:
        success (bool): Indicates if the request was successful.
        endpoint (str): The name or path of the endpoint.
        data (dict, optional): Additional data or results from the endpoint. Default is None.
    """
    success: bool
    endpoint: str
    data: dict = None
    
 

        
def get_predict_log(input_data: List[InputData], output_data: dict,model_name,
                    model_version,model_alias=None):
    """
    Create and return a JSON-formatted log entry for prediction requests and outputs.

    This function pairs each input data item with its corresponding output prediction and includes 
    details about the model used for the prediction. The result is formatted as a JSON string.

    Args:
        input_data (List[InputData]): A list of input data instances.
        output_data (List[OutputData]): A list of output data instances corresponding to the input data.
        model_name (str): The name of the prediction model.
        model_version (str): The version of the prediction model.

    Returns:
        str: A JSON-formatted string summarizing the prediction data and results.
    """
    summarized_data = []
    for inp, out in zip(input_data, output_data):
        summarized_item = {
            # Convert input data to a dictionary
            #"input": inp.dict(),
            "input": inp.model_dump(),
            # Extract price from OutputData
            "predicted_price": out,
            "model_name": model_name,
            "model_version": model_version,
        }
        if model_alias:
            summarized_item['model_alias']=model_alias
        summarized_data.append(summarized_item)

    return json.dumps(summarized_data, indent=2)  # Convert to a JSON string for logging



def monitor_input_metrics(data: List[InputData], input_logger, generic_logger):
    """
    Monitor and log any anomalies found in the input data.

    This function checks for invalid conditions in the input data, such as non-positive values for
    certain numeric fields. It aggregates all warnings and logs them in a single entry for efficiency.

    Args:
        data (List[InputData]): A list of input data instances to be monitored.
        input_logger: The logger for recording input-specific logs.
        generic_logger: The logger for recording general logs.

    Raises:
        Exception: If any error occurs during the monitoring process.
    """
    warning_messages = []
    try:
        for item in data:
         # Check for specific condition
            if item.net_usable_area <= 0:
                 warning_messages.append(f"net_usable_area value: {item.net_usable_area} in request (expecting >0)")
            if item.net_area<=0:
                 warning_messages.append(f"net_area value: {item.net_area} in request (expecting >0)")
            if item.n_rooms<=0:
                 warning_messages.append(f"n_rooms value: {item.n_rooms} in request (expecting >0)")
            if item.n_bathroom<=0:
                 warning_messages.append(f"n_bathroom value: {item.n_bathroom} in request (expecting >0)")
        if warning_messages:
            input_logger.warning(f"Anomalies detected in input data: {', '.join(warning_messages)}")    
    except Exception as e:
        input_logger.error(f"Error during metrics validation: {e}")
        generic_logger.warning(f"Error during metrics validation: {e}")
