from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {
                "success": False,
                "status_code": 500,
                "message": "Internal server error.",
                "errors": None
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    status_code = response.status_code

    if status_code == 400:
        message = "Validation failed."
    elif status_code == 401:
        message = "Authentication required."
    elif status_code == 403:
        message = "Permission denied."
    elif status_code == 404:
        message = "Resource not found."
    elif status_code == 405:
        message = "Method not allowed."
    else:
        message = "An error occurred."

    response.data = {
        "success": False,
        "status_code": status_code,
        "message": message,
        "errors": response.data
    }

    return response
