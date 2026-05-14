import logging
import uuid

logger = logging.getLogger("app")


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.request_id = request_id

        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "path": request.path,
                "method": request.method,
            },
        )

        response = self.get_response(request)
        response["X-Request-ID"] = request_id

        logger.info(
            "Request finished",
            extra={
                "request_id": request_id,
                "path": request.path,
                "method": request.method,
            },
        )

        return response
