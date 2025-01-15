# FastAPI Project Setup Guide using `uv` 🚀✨💡

I've been tinkering with FastAPI and have found a couple of useful repos. However there are so many different tools and styles in use, I found it hard to bootstrap and start my projects. This guide provides a step-by-step process for scaffolding a **FastAPI** project using **`fastapi-users`** for authentication and authorization, **PostgreSQL** as the database, **Alembic** for migrations, and **`uv`** for package management. I will try to build this out over time as I incorporate additional tools/techniques. I'm learning a lot from the [zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices) repository. 🌟🔧📄

---

## 1. Project Initialization 🛠️📂🔧

### 1.1 Install `uv` 🖥️💻✨

Ensure that Python 3.7+ is installed, then globally install `uv`:

```bash
pip install uv
```

Verify the installation:

```bash
uv --version
```

### 1.2 Initialize a New Project 🚀📂⚡

Create a new directory for the project and initialize it using `uv`:

```bash
mkdir fastapi-project
cd fastapi-project
uv init
```

This command creates a `pyproject.toml` file for managing dependencies. 📝📦🔧

### 1.3 Add Required Dependencies 🧰📦⚙️

Add the following dependencies using `uv`:

```bash
uv add fastapi uvicorn psycopg2-binary python-dotenv alembic passlib bcrypt
uv add fastapi-users --extra sqlalchemy
```

`uv` will install and pin the specified versions of the packages while updating `pyproject.toml` automatically. 📋✨🔒

---

## 2. Directory Structure 📂🏗️✨

Here’s the recommended directory structure based on best practices:

```plaintext
fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── models.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── manager.py
│   │   └── schemas.py
│   └── api/
│       ├── __init__.py
│       └── routes.py
├── alembic/
│   └── versions/
├── alembic.ini
└── .env
```

---

## 3. Environment Variables (`.env`) 🌍🔐📄

Create a `.env` file to store environment variables:

```ini
DATABASE_URL=postgresql://username:password@localhost:5432/mydatabase
SECRET_KEY=your_secret_key_here
```

---

## 4. Database Configuration (`app/db/base.py`) 🗄️⚙️🔗

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()
```

---

## 5. User Model and Schemas 👤📄🔧

### 5.1 User Schemas (`app/users/schemas.py`) 🧾📚✨

```python
from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass
```

### 5.2 User Table (`app/db/models.py`) 🛠️📊🗄️

```python
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String
from sqlalchemy import Integer
from ..db.base import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
```

---

## 6. User Manager (`app/users/manager.py`) 👨‍💻🔑📜

```python
from fastapi_users import BaseUserManager, IntegerIDMixin
from .schemas import UserCreate
from ..db.models import User
from ..db.base import SessionLocal
import os

SECRET_KEY = os.getenv("SECRET_KEY")

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request=None):
        print(f"User {user.email} has registered.")

def get_user_manager():
    db = SessionLocal()
    yield UserManager(db)
```

---

## 7. Auth Setup (`app/users/auth.py`) 🔒🔑📋

```python
from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from .schemas import UserRead, UserCreate, UserUpdate
from .manager import get_user_manager
from ..db.models import User

SECRET_KEY = os.getenv("SECRET_KEY")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
```

---

## 8. API Routes (`app/api/routes.py`) 🚦📡🔧

```python
from fastapi import APIRouter
from ..users.auth import fastapi_users, auth_backend
from ..users.schemas import UserRead, UserCreate, UserUpdate

router = APIRouter()

# User routes
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
```

---

## 9. Main Application (`app/main.py`) 🖥️🚀🔧

```python
from fastapi import FastAPI
from .api.routes import router as api_router
from .db.base import Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API router
app.include_router(api_router)
```

---

## 10. Alembic Setup ⚙️🗂️📋

### 10.1 Initialize Alembic 🏗️🔧📝

```bash
alembic init alembic
```

### 10.2 Configure Alembic 🛠️🗄️✨

Edit `alembic.ini` and set the `sqlalchemy.url` to the database URL from `.env`. Additionally, update `env.py` to include the `target_metadata` from your models by importing the `Base` class and setting `target_metadata = Base.metadata`. This ensures Alembic can detect schema changes correctly during migrations:

```ini
sqlalchemy.url = postgresql://username:password@localhost:5432/mydatabase
```

```python
from app.db.base import Base

target_metadata = Base.metadata
```

### 10.3 Create and Apply Migrations 🚀📋✨

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

## 11. Run the Application 🚀🖥️🌐

Start the FastAPI application using `uv`:

```bash
uv run app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to test the API using the automatically generated interactive documentation. 🌐📋✨

---

## 12. Managing Dependencies with `uv` 📦🛠️🔄

### Add a New Dependency ➕📦✨

```bash
uv add <package-name>
```

### Update Dependencies 🔄⚙️📦

```bash
uv update
```

### Remove a Dependency ➖🗑️📦

```bash
uv remove <package-name>
```

---