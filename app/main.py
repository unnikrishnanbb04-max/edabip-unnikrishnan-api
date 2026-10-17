
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import settings
from app.database import Base, engine
from app import models
from app.routers import auth, dashboard, reports, activity, templates, schedules


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(activity.router)
app.include_router(templates.router)
app.include_router(schedules.router)


@app.get("/")
def health_check():
    return {"message": "Reports API is running"}
