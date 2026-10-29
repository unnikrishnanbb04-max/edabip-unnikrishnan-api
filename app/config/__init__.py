from app.config.settings import settings


def get_cors_origins() -> list[str]:
    return [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]


__all__ = ["settings", "get_cors_origins"]
