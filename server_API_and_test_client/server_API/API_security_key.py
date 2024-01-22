"""
This module provides security features for a FastAPI application, specifically for API key validation.
It includes the functionality to define an API key header, load API keys from environment variables, 
and validate the API key provided in the request headers against the expected key. The environment variables 
are loaded from a `.env` file, ensuring that sensitive information like API keys are not hard-coded into the
application.

Functions:
- validate_api_key: Validates the provided API key against the expected key.
"""

from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Depends
import os
from pathlib import Path
from dotenv import load_dotenv

# Define the API Key Header
api_key_header = APIKeyHeader(name="House-Price-API-KEY", auto_error=False)

# Load API environment variables from .env file
key_path=  Path('keys') /'keys_app.env'
load_dotenv(key_path)


# Dependency
async def validate_api_key(api_key: str = Depends(api_key_header)):
    """
    Validate the provided API key against the expected API key.

    This function checks the API key provided in the request header. If the key matches the key
    stored in the environment variable, access is granted. Otherwise, an HTTP 403 Forbidden exception
    is raised, indicating invalid credentials.

    Args:
        api_key (str): The API key retrieved from the request header.

    Returns:
        bool: True if the API key is valid, otherwise raises HTTPException.

    Raises:
        HTTPException: 403 error if the API key does not match.
    """
    
    if api_key == os.getenv("APP_Key_5839123"): #APP_Key_5839123 is the variable name and not the key value
        return True
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")
