"""Функции безопасности для проекта инцидентов."""

from src.core.config import settings


def verify_x_access_key(access_key: str) -> bool:
    """Проверить валидность X-Access-Key."""
    return access_key == settings.x_access_key
