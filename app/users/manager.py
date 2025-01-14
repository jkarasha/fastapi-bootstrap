import os
#
from fastapi_users import BaseUserManager, IntegerIDMixin
from .schemas import UserCreate
from ..db.models import User
from ..db.base import SessionLocal

SECRET_KEY = os.getenv("SECRET_KEY")

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request=None):
        print(f"User {user.email} has registered!")

def get_user_manager():
    db = SessionLocal()
    yield UserManager(db)