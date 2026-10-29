
import csv
from io import StringIO

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models import User, Report
from app.main import app
from tests.conftest import token
from app.security import hash_password
from app.routers.auth import _attempts, _lock



TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=TEST_ENGINE,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=TEST_ENGINE)
    Base.metadata.create_all(bind=TEST_ENGINE)

    db = TestingSessionLocal()

    admin = User(
        name="Test Admin",
        email="admin@example.com",
        hashed_password=hash_password("AdminPass123"),
        role="Admin",
    )
    viewer = User(
        name="Test Viewer",
        email="viewer@example.com",
        hashed_password=hash_password("ViewerPass123"),
        role="Viewer",
    )

    db.add_all([admin, viewer])
    db.commit()

    report = Report(
        report_name="Sales Report",
        module="Sales",
        report_type="On Demand",
        owner="Test Admin",
        status="Completed",
        run_duration_seconds=1.2,
    )
    db.add(report)
    db.commit()
    db.close()

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    with _lock:
        _attempts.clear()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=TEST_ENGINE)


def get_token(client, email, password):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_login_returns_jwt(client):
    token = get_token(client, "admin@example.com", "AdminPass123")
    assert len(token) > 20


def test_report_requires_token(client):
    response = client.get("/reports/")
    assert response.status_code == 401


def test_viewer_cannot_rerun_report(client):
    token = get_token(
        client,
        "viewer@example.com",
        "ViewerPass123",
    )

    response = client.post(
        "/reports/1/rerun",
        headers=auth_header(token),
    )

    assert response.status_code == 403


def test_invalid_pagination_returns_422(client):
    token = get_token(client, "viewer@example.com", "ViewerPass123")
    response = client.get(
        "/reports/?page=0",
        headers=auth_header(token),
    )
    assert response.status_code == 422


def test_missing_report_returns_404(client):
    token = get_token(client, "viewer@example.com", "ViewerPass123")
    response = client.get(
        "/reports/9999",
        headers=auth_header(token),
    )
    assert response.status_code == 404


def test_csv_contains_header_row(client):
    token = get_token(
        client,
        "viewer@example.com",
        "ViewerPass123",
    )

    response = client.get(
        "/reports/activity/export.csv",
        headers=auth_header(token),
    )

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]

    rows = list(csv.reader(StringIO(response.text)))

    assert rows[0] == [
        "id",
        "report_id",
        "schedule_id",
        "action",
        "status",
        "message",
        "duration_seconds",
        "created_at",
    ]

def test_viewer_can_list_reports(client):
    token = get_token(client, "viewer@example.com", "ViewerPass123")
    response = client.get(
        "/reports/",
        headers=auth_header(token),
    )
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_invalid_sort_column_returns_422(client):
    token = get_token(client, "viewer@example.com", "ViewerPass123")
    response = client.get(
        "/reports/?sort_by=password",
        headers=auth_header(token),
    )
    assert response.status_code == 422


def test_viewer_cannot_delete_report(client):
    token = get_token(client, "viewer@example.com", "ViewerPass123")
    response = client.delete(
        "/reports/1",
        headers=auth_header(token),
    )
    assert response.status_code == 403
