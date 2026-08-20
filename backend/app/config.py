import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Diploma Task App")
    app_version: str = os.getenv("APP_VERSION", "dev")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
    cors_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://localhost:8080"
        ).split(",")
        if origin.strip()
    )


settings = Settings()
