
reports-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── exceptions.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── report.py
│   │   ├── template.py
│   │   ├── activity.py
│   │   └── schedule.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── report.py
│   │   ├── template.py
│   │   ├── activity.py
│   │   └── schedule.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── report_repository.py
│   │   ├── template_repository.py
│   │   ├── activity_repository.py
│   │   └── schedule_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── report_service.py
│   │   ├── dashboard_service.py
│   │   └── schedule_service.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── dashboard.py
│       ├── reports.py
│       ├── activity.py
│       ├── templates.py
│       └── schedules.py
│
├── sql/
│   ├── schema.sql
│   └── seed.sql
│
├── tests/
│   ├── __init__.py
│   └── test_reports.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

module not foundedd eror 
python -m pip install pydantic-settings
python -m pip install "python-jose[cryptography]"
python -m pip install "passlib[bcrypt]"
 uvicorn app.main:app --reload
 tests cases run comand
 python -m pytest tests/test_reports.py -v