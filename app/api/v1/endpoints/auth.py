from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    decode_access_token_for_refresh,
)
from app.models.user import Token, User, UserCreate
from app.services import user_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate):
    """
    Create a new user (in-memory only).
    """
    try:
        return user_service.create_user(user_in)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return a JWT access token.
    """
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.email, expires_delta=access_token_expires)
    return Token(access_token=access_token)


@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
def refresh_access_token(token: str = Depends(oauth2_scheme)):
    """
    Refresh an access token using the current token.
    """
    email = decode_access_token_for_refresh(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or malformed token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Verify user still exists
    user_in_db = user_service.get_user_by_email(email)
    if user_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Issue new token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        subject=email, expires_delta=access_token_expires
    )
    return Token(access_token=new_access_token)


@router.get("/_debug_users")
def list_users_debug():
    """
    TEMP: List all in-memory users for debugging.
    """
    return [
        {
            "email": u.email,
            "hashed_password": u.hashed_password,
        }
        for u in user_service._fake_users_db.values()
    ]
