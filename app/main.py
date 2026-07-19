from fastapi import FastAPI

from app.database import Base, engine
from app import models

from app.routes.send import router as send_router

from app.routes import tracking


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Email Tracking Service"
)

app.include_router(send_router)


@app.get("/")
def home():
    return {"message": "Email Tracking Service is running 🚀"}

app.include_router(tracking.router)