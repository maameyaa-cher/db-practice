from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.middleware import LoggingMiddleware

# Setup logging
setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

# Add middleware
app.add_middleware(LoggingMiddleware)

app.include_router(api_router, prefix="/api/v1")