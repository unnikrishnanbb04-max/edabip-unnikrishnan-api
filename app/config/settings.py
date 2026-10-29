from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Reports API"
    database_url: str = "mysql+pymysql://root:Sureshjeya%40123@localhost:3306/reports_db"
    secret_key: str = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    access_token_minutes: int = 60
    cors_origins: str = "http://localhost:5173"
    scheduler_interval_seconds: int = 60
    login_rate_limit_attempts: int = 10
    login_rate_limit_window_seconds: int = 60
    run_scheduler: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


    @property
    def rate_limit_login(self) -> str:
        if self.login_rate_limit_window_seconds == 60:
            return f"{self.login_rate_limit_attempts}/minute"
        if self.login_rate_limit_window_seconds == 3600:
            return f"{self.login_rate_limit_attempts}/hour"
        if self.login_rate_limit_window_seconds == 86400:
            return f"{self.login_rate_limit_attempts}/day"

        raise ValueError(
            "Unsupported login rate-limit window. "
            "Use 60, 3600, or 86400 seconds."
        )

    @property
    def scheduler_enabled(self) -> bool:
        return self.run_scheduler



settings = Settings()
