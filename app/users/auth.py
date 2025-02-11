import os
import uuid
from fastapi import Depends
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
#
from app.users.schemas import UserRead, UserCreate, UserUpdate
from app.users.manager import get_user_manager

from app.users.models import User

SECRET_KEY = os.getenv("SECRET_KEY")

def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend]
)

current_active_user = fastapi_users.current_user(active=True)