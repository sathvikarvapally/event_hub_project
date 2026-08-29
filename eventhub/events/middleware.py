import time
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware to log the request and response details.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the incoming request details
        logger.info(f"Incoming request: {request.method} {request.get_full_path()}")

        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        # Log the outgoing response details
        logger.info(f"Outgoing response: {response.status_code} for {request.method} {request.get_full_path()} (Duration: {duration:.2f}s)")

        return response