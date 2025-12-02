import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add structured logging and request context to every request.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Clear context and bind initial request details
        clear_contextvars()
        request_id = str(uuid.uuid4())
        bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else "unknown",
        )

        start_time = time.time()
        log = structlog.get_logger()

        log.info("Request started")

        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            status_code = response.status_code
        except Exception as e:
            log.exception("Request failed")
            status_code = 500
            response = Response("Internal Server Error", status_code=500)
        
        duration = time.time() - start_time
        bind_contextvars(status_code=status_code, duration_ms=round(duration * 1000, 2))
        log.info("Request finished")

        return response
