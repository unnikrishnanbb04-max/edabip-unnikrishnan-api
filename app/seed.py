from datetime import datetime, timedelta, timezone
from app.database import SessionLocal
from app.models import Report, ReportTemplate, User, ReportActivity
from app.security import hash_password

def seed():
    db = SessionLocal()
    try:
        if db.query(Report).count() > 0:
            print("Seed skipped: reports already exist.")
            return
        templates = []
        for name, module in [
            ("Monthly Revenue", "Finance"), ("User Engagement", "Analytics"),
            ("Inventory Snapshot", "Operations"), ("Support SLA", "Support"),
            ("Security Audit", "Security")
        ]:
            item = ReportTemplate(template_name=name, module=module, description=f"{name} report template")
            db.add(item); templates.append(item)
        db.flush()
        admin = User(name="Demo Admin", email="admin@example.com", hashed_password=hash_password("AdminPass123!"), role="Admin")
        viewer = User(name="Demo Viewer", email="viewer@example.com", hashed_password=hash_password("ViewerPass123!"), role="Viewer")
        db.add_all([admin, viewer]); db.flush()
        now = datetime.now(timezone.utc)
        for i in range(1, 31):
            status = ["Completed", "Failed", "Scheduled"][i % 3]
            report = Report(report_name=f"Sample Report {i:02d}", module=templates[(i-1)%len(templates)].module,
                            report_type="Scheduled" if i % 2 == 0 else "On Demand", status=status,
                            owner=["Asha", "Ravi", "Meena", "Arun"][i%4],
                            last_run=now-timedelta(hours=i) if status != "Scheduled" else None,
                            run_duration_seconds=float(10 + i) if status == "Completed" else None,
                            created_at=now-timedelta(days=i), template_id=templates[(i-1)%len(templates)].id)
            db.add(report)
        db.commit()
        print("Seeded 30 reports, 5 templates, and demo users.")
        print("Admin login: admin@example.com / AdminPass123!")
        print("Viewer login: viewer@example.com / ViewerPass123!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
