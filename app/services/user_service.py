from typing import Dict, Optional

from app.core.security import get_password_hash, verify_password
from app.models.user import UserInDB, UserCreate, User

# For demo purposes only.
_fake_users_db: Dict[str, UserInDB] = {}


def get_user_by_email(email: str) -> Optional[UserInDB]:
    return _fake_users_db.get(email.lower())


def create_user(user_in: UserCreate) -> User:
    email = user_in.email.lower()
    if email in _fake_users_db:
        raise ValueError("User already exists")
    hashed_password = get_password_hash(user_in.password)
    user = UserInDB(email=email, hashed_password=hashed_password)
    _fake_users_db[email] = user
    return User(email=email)


def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    user = get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
