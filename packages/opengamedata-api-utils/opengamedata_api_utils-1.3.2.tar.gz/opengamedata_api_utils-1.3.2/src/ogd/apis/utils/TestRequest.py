import logging
import requests
from typing import Any, Dict, Optional

def TestRequest(url:str, request:str, params:Optional[Dict[str, Any]]=None, body:Optional[Dict[str, Any]]=None, timeout:int=1, logger:Optional[logging.Logger]=None) -> requests.Response:
    """Utility function to make it easier to send requests to a remote server during unit testing.

    This function does some basic sanity checking of the target URL,
    maps the request type to the appropriate `requests` function call,
    and performs basic error handling to notify what error occurred.

    :param url: The target URL for the web request
    :type url: str
    :param request: Whether to perform a "GET", "POST", or "PUT" request
    :type request: str
    :param params: A mapping of request parameter names to values. Defaults to {}
    :type params: Dict[str, Any], optional
    :param body: The body of the request to send. Defaults to None
    :type body: Dict[str, Any], optional
    :param logger: A logger to use for debug/error outputs. Defaults to None
    :type logger: logging.Logger, optional
    :raises err: Currently, any exceptions that occur during the request will be raised up.
        If verbose logging is on, a simple debug message indicating the request type and URL is printed first.
    :return: The `Response` object from the request, or None if an error occurred.
    :rtype: requests.Response
    """
    ret_val : requests.Response

    params = params or {}

    if not (url.startswith("https://") or url.startswith("http://")):
        url = f"https://{url}" # give url a default scheme
    try:
        match (request.upper()):
            case "GET":
                ret_val = requests.get(url, params=params, timeout=timeout)
            case "POST":
                ret_val = requests.post(url, params=params, data=body, timeout=timeout)
            case "PUT":
                ret_val = requests.put(url, params=params, data=body, timeout=timeout)
            case _:
                if logger:
                    logger.warning(f"Bad request type {request}, defaulting to GET")
                ret_val = requests.get(url, params=params, timeout=timeout)
    except Exception as err:
        if logger:
            logger.error(f"Error on {request} request to {url} : {err}")
        raise err
    else:
        if logger:
            logger.debug(f"Request sent to:        {url}")
            logger.debug(f"Response received from: {ret_val.url}")
            logger.debug(f"   Status: {ret_val.status_code}")
            logger.debug(f"   Data:   {ret_val.text}")
        return ret_val
