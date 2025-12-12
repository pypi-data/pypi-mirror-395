"""
Internet - HTTP requests that just WORK

Usage:
    from internet import *
    
    # Single URL
    data = get.data(url)
    
    # Multiple URLs (10x faster!)
    results = get.many([url1, url2, url3])
    
    # Sleep for X seconds
    waitfor(2)
    
    # Run async function
    result = runfor(some_async_function())
"""

from .getter import get
import asyncio

def waitfor(seconds):
    """
    Pause execution for X seconds
    
    Args:
        seconds (int/float): How long to wait
        
    Example:
        >>> waitfor(2)  # Pause for 2 seconds
    """
    import time
    time.sleep(seconds)

def runfor(async_function):
    """
    Run an async function
    
    Args:
        async_function: The async function to run
        
    Returns:
        Result of the async function
        
    Example:
        >>> result = runfor(some_async_function())
    """
    return asyncio.run(async_function)

__version__ = "1.2.0"
__all__ = ['get', 'waitfor', 'runfor']
