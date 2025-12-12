import functools
from typing import Callable

from flask import jsonify, Response, make_response
import traceback

def make_http_response(job_func: Callable) -> Callable:
    """ This decorator makes the response of the cloud function a flask response object. """
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            return_value = job_func(*args, **kwargs)
        except:
            return make_response(jsonify(details=traceback.format_exc()), 500)

        if isinstance(return_value, (tuple, list)):
            if len(return_value) != 2:
                unsupported_return_msg = f'Unsupported return {return_value} for args {args}, {kwargs} in {job_func.__name__}'
                return make_response(jsonify(details=unsupported_return_msg), 500)
            if isinstance(return_value[1], int):
                response: Response = jsonify(return_value[0])
                response.status_code = return_value[1]
                return response
            if isinstance(return_value[0], int):
                response: Response = jsonify(return_value[1])
                response.status_code = return_value[0]
                return response
            no_status_code_msg = f'One of the return should be a status code. Bad return {return_value} for args {args}, {kwargs} in {job_func.__name__}'
            return make_response(jsonify(details=no_status_code_msg), 500)
        if return_value is None:
            return Response(status=200)
        if isinstance(return_value, int):
            return Response(status=return_value)
        return jsonify(return_value)
    return wrapper

