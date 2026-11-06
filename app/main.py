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
from app.seed import Seed
# import app.models  # ensure models are registered with SQLAlchemy metadata

import json
from pathlib import Path

from fastapi.openapi.utils import get_openapi


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

Seed()  # Seed the database with initial data if not already present

# Generate OpenAPI schema
openapi_schema = get_openapi(
    title=app.title,
    version=app.version,
    description=app.description,
    routes=app.routes,
)

# Embed schema directly into HTML
schema_json = json.dumps(openapi_schema).replace("</", "<\\/")

# Swagger UI HTML
swagger_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{app.title} - Swagger UI</title>
    <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <style>
        body {{ margin: 0; background: #fafafa; }}
        .topbar {{ display: none; }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>

    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        const spec = {schema_json};

        SwaggerUIBundle({{
            spec: spec,
            dom_id: "#swagger-ui",
            deepLinking: true,
            displayRequestDuration: true,
            filter: true,
            docExpansion: "list",
            defaultModelsExpandDepth: 2,
            defaultModelExpandDepth: 2,
            persistAuthorization: true
        }});
    </script>
</body>
</html>
"""


# ReDoc HTML
redoc_html =f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{app.title} - ReDoc</title>
    <style>
        body {{ margin: 0; padding: 0; }}
    </style>
</head>
<body>
    <redoc id="redoc-container"></redoc>

    <script src="https://cdn.jsdelivr.net/npm/redoc@2.5.4/bundles/redoc.standalone.js"></script>
    <script>
        const spec = {schema_json};

        Redoc.init(
            spec,
            {{
                scrollYOffset: 0,
                hideDownloadButton: false,
                expandResponses: "200,201",
                requiredPropsFirst: true,
                sortPropsAlphabetically: true,
                pathInMiddlePanel: true,
                theme: {{
                    colors: {{
                        primary: {{
                            main: "#2563eb"
                        }}
                    }}
                }}
            }},
            document.getElementById("redoc-container")
        );
    </script>
</body>
</html>
"""

Path("docs.html").write_text(swagger_html, encoding="utf-8")
Path("redoc.html").write_text(redoc_html, encoding="utf-8")

print("Generated docs.html and redoc.html successfully!")
