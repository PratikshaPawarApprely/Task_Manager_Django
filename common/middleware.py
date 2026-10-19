import time
import uuid


class RequestLoggingMiddleware:

    SLOW_API_THRESHOLD = 1.0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid.uuid4())
        )

        request.request_id = request_id

        start_time = time.time()

        response = self.get_response(request)

        execution_time = time.time() - start_time

        response["X-Request-ID"] = request_id

        print(
            f"[{request_id}] "
            f"{request.method} "
            f"{request.path} "
            f"{response.status_code} "
            f"{execution_time:.4f}s"
        )

        if execution_time > self.SLOW_API_THRESHOLD:
            print(
                f"SLOW API: "
                f"{request.method} "
                f"{request.path} "
                f"took {execution_time:.4f}s"
            )

        return response