import os
os.environ["DATABASE_URL"] = "sqlite:///./test_reports.db"
os.environ["RUN_SCHEDULER"] = "false"
os.environ["SECRET_KEY"] = "test-secret-key-that-is-long-enough-for-tests"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app
from app.models import User, Report, ReportTemplate, ReportSchedule
from app.security import hash_password

@pytest.fixture()
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(engine)
    def override_db():
        db = TestingSession()
        try: yield db
        finally: db.close()
    app.dependency_overrides[get_db] = override_db
    with TestingSession() as db:
        template = ReportTemplate(template_name="Finance Template", module="Finance", description="test")
        db.add(template); db.flush()
        admin = User(name="Admin User", email="admin@test.com", hashed_password=hash_password("AdminPass123!"), role="Admin")
        viewer = User(name="Viewer User", email="viewer@test.com", hashed_password=hash_password("ViewerPass123!"), role="Viewer")
        db.add_all([admin, viewer]); db.flush()
        db.add(Report(report_name="Test Revenue", module="Finance", report_type="Scheduled", status="Scheduled", owner="Admin", template_id=template.id))
        db.commit()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()

def token(client, email="admin@test.com", password="AdminPass123!"):
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture()
def admin_headers(client):
    return {"Authorization": f"Bearer {token(client)}"}

@pytest.fixture()
def viewer_headers(client):
    return {"Authorization": f"Bearer {token(client, 'viewer@test.com', 'ViewerPass123!')}"}
