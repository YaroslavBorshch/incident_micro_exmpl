from typing import Dict, Any

from src.services.kafka_service import kafka_producer


class TelegramService:
    """получение сообщений из Telegram и отправка уведомлений"""

    def __init__(self):
        self._kafka_producer = kafka_producer

    async def initialize(self):
        pass

    async def close(self):
        pass

    async def handle_telegram_message(self, message_data: Dict[str, Any]):
        await self._kafka_producer.publish_incident(message_data)

    async def send_incident_notification(self, incident_data: Dict[str, Any]):
        pass


telegram_service = TelegramService()
