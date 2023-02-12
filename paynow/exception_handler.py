import json

from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from requests.exceptions import HTTPError
from datetime import datetime
from datetime import timezone

import logging
logger = logging.getLogger(__name__)

def handler(exc, context):

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

    if isinstance(exc, ValidationError):
        error = exc.detail
        message = ""
        fieldKey = ""
        for key in error:
            message = error[key][0]
            fieldKey = key
            break

        if message is not None or message != "" and "This" in message:
            message = message.replace("This", "'{}'".format(fieldKey), 1)
        data = {"message": str(message)}
        print(data)
        response = Response(data, status=exc.status_code)
        return response


    if isinstance(exc, Exception):
        status = None
        try:
            status = exc.status_code

        except Exception as e:
            status = 422
        data = {"message": str(exc)}
        print(data)
        response = Response(data, status=status)

    return response
