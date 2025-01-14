from fastapi import FastAPI
from .api.routes import router as api_router
from .db.base import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router)