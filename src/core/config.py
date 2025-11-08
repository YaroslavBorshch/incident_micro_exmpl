from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """настройки проекта"""

    # Значения по умолчанию используются, если в .env нет соответствующих переменных
    # Переменные из .env автоматически переопределяют значения по умолчанию
    # Приоритет: переменные окружения > .env файл > значения по умолчанию

    # database settings
    database_url: str = "postgresql://root:root@localhost:5432/incedent"

    redis_url: str = "redis://localhost:6379"

    # X-Access-Key authentication
    x_access_key: str = "development-access-key"

    # Cache settings
    cache_enabled: bool = True
    cache_max_memory: str = "256mb"
    cache_eviction_policy: str = "allkeys-lru"
    cache_incidents_ttl: int = 600  # 10 minutes

    # Kafka settings...

    # Telegram settings...

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Переменные окружения не чувствительны к регистру
    )

    @property
    def asyncpg_uri(self) -> str:
        """Получить URI с asyncpg драйвером."""
        s = str(self.database_url)

        if "asyncpg" not in s:
            return s.replace("postgresql", "postgresql+asyncpg", 1)

        return s


settings = Settings()
