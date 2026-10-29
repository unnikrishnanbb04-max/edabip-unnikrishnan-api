def test_health(client):
    assert client.get("/health").json()["status"] == "ok"

def test_register(client):
    r = client.post("/auth/register", json={"name":"New User","email":"new@test.com","password":"Password123","role":"Viewer"})
    assert r.status_code == 201
    assert "hashed_password" not in r.json()

def test_login(client):
    assert client.post("/auth/login", json={"email":"admin@test.com","password":"AdminPass123!"}).status_code == 200

def test_missing_token_401(client):
    assert client.get("/reports/summary").status_code == 401

def test_viewer_rerun_403(client, viewer_headers):
    assert client.post("/reports/1/rerun", headers=viewer_headers).status_code == 403

def test_bad_report_input_422(client, admin_headers):
    assert client.post("/reports", headers=admin_headers, json={"report_name":"x"}).status_code == 422

def test_unknown_report_404(client, admin_headers):
    assert client.get("/reports/999", headers=admin_headers).status_code == 404

def test_summary(client, admin_headers):
    r = client.get("/reports/summary", headers=admin_headers)
    assert r.status_code == 200
    assert r.json()["total_reports"] == 1

def test_csv_header(client, admin_headers):
    r = client.get("/reports/activity/export.csv", headers=admin_headers)
    assert r.status_code == 200
    assert r.text.splitlines()[0] == "id,report_id,schedule_id,action,status,message,duration_seconds,created_at"

def test_report_list_pagination(client, admin_headers):
    r = client.get("/reports?page=1&size=5", headers=admin_headers)
    assert r.status_code == 200
    assert set(["items","total","page","size"]).issubset(r.json())

def test_create_schedule(client, admin_headers):
    r = client.post("/schedules", headers=admin_headers, json={"report_id":1,"frequency":"Daily","next_run":"2020-01-01T00:00:00Z","is_active":True})
    assert r.status_code == 201

def test_schedule_not_found(client, admin_headers):
    assert client.get("/schedules/999", headers=admin_headers).status_code == 404

def test_sort_validation(client, admin_headers):
    assert client.get("/reports?sort_by=raw_sql", headers=admin_headers).status_code == 422
