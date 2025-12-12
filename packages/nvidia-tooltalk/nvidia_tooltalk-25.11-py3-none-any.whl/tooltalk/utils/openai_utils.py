"""
Copyright (c) Microsoft Corporation.
Licensed under the MIT license.
"""
import logging
import time
from functools import wraps
from urllib.parse import urlparse

from openai import OpenAI, RateLimitError

logger = logging.getLogger(__name__)

# Singleton client instance
_client = None

def get_client(api_key=None, base_url=None):
    """Get or create the OpenAI client instance."""
    global _client
    if _client is None or api_key is not None or base_url is not None:
        if not api_key:
            raise ValueError("API key is required")
        _client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
    return _client

def retry_on_limit(func, retries=5, wait=60):
    """Retry a function on rate limit errors."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except RateLimitError as error:
                logger.info(str(error))
                time.sleep(wait)
        raise RateLimitError
    return wrapper

@retry_on_limit
def openai_chat_completion(*args, **kwargs):
    """Make a chat completion request with retry logic."""
    # Extract base_url and api_key from kwargs
    base_url = kwargs.pop('base_url', None)
    api_key = kwargs.pop('api_key', None)
    
    # Get or create client
    client = get_client(api_key, base_url)
    
    try:
        return client.chat.completions.create(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        raise

@retry_on_limit
def openai_completion(*args, **kwargs):
    """Make a completion request with retry logic."""
    # Extract base_url and api_key from kwargs
    base_url = kwargs.pop('base_url', None)
    api_key = kwargs.pop('api_key', None)
    
    # Get or create client
    client = get_client(api_key, base_url)
    
    try:
        return client.completions.create(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in completion: {str(e)}")
        raise
