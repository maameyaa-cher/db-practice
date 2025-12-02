from fastapi import APIRouter

from app.api.v1.endpoints import health, items, forms, auth

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(items.router, tags=["items"])
api_router.include_router(forms.router, prefix="/forms", tags=["forms"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
