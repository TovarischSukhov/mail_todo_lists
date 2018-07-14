# coding=utf-8

from functools import wraps
from flask import make_response, jsonify, request

STATUSES = {
    'HTTP_403_forbidden': 403,
    'HTTP_200_ok': 200,
    'HTTP_400_bad_request': 400,
}


def success_response(data=None):
    return make_response(
        jsonify(
            {
                'success': True,
                'data': data or {}
            }
        ),
        200
    )


def error_response(error, status):
    return make_response(
        jsonify(
            {
                'success': False,
                'data': {
                    'error': error
                }
            }
        ),
        status
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('x-service')
        if not auth:
            return error_response('x-service header with your service name is required', 403)
        return f(*args, **kwargs)
    return decorated
