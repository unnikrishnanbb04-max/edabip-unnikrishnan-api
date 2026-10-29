from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Reports API"
    database_url: str = "postgresql+psycopg://reports:reports@db:5432/reports"
    secret_key: str = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
    algorithm: str = "HS256"
    access_token_minutes: int = 30
    cors_origins: str = "http://localhost:5173"
    scheduler_interval_seconds: int = 60
    login_rate_limit_attempts: int = 10
    login_rate_limit_window_seconds: int = 60
    run_scheduler: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

def get_cors_origins() -> list[str]:
    return [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
