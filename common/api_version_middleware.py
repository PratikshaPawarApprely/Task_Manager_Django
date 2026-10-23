from datetime import date
from django.http import JsonResponse


class APIVersionSunsetMiddleware:
    SUNSET_DATE = date(2027, 1, 1)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path.startswith("/api/v1/")
            and date.today() >= self.SUNSET_DATE
        ):
            return JsonResponse(
                {
                    "success": False,
                    "message": (
                        "API Version 1 is no longer available. "
                        "Please use API Version 2."
                    ),
                    "latest_version": "/api/v2/",
                },
                status=410,
            )

        return self.get_response(request)
