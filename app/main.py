import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import settings, get_cors_origins
from app.database import Base, engine
from app.middleware import request_id_middleware
from app.routers import auth, reports, schedules, templates
from app.services.scheduler import scheduler_tick
import app.models  # ensure models are registered with SQLAlchemy metadata

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
scheduler = BackgroundScheduler(timezone="UTC")

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.run_scheduler:
        scheduler.add_job(scheduler_tick, "interval", seconds=settings.scheduler_interval_seconds,
                          id="report-scheduler", replace_existing=True, max_instances=1)
        scheduler.start()
    yield
    if scheduler.running:
        scheduler.shutdown(wait=False)

app = FastAPI(title=settings.app_name, version="1.0.0", description="Reports API with authentication, schedules, CSV export and execution history", lifespan=lifespan)
@app.get("/health", tags=["Health"], summary="Check API health")
def health():
    return {"status":"ok"}

app.middleware("http")(request_id_middleware)
app.add_middleware(CORSMiddleware, allow_origins=get_cors_origins(), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router)
app.include_router(reports.router)
app.include_router(schedules.router)
app.include_router(templates.router)


