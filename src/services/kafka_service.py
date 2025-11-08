from typing import Dict, Any, Optional


class KafkaProducerService:
    """публикация сообщений в Kafka топик"""

    def __init__(self):
        pass

    async def initialize(self):
        pass

    async def close(self):
        pass

    async def publish_incident(self, message_data: Dict[str, Any]):
        pass


class KafkaConsumerService:
    """чтение и обработка сообщений из Kafka топика"""

    def __init__(self):
        self._telegram_service: Optional[Any] = None

    async def initialize(self):
        from src.services.telegram_service import telegram_service
        self._telegram_service = telegram_service

    async def close(self):
        pass

    async def consume_incidents(self):
        pass


kafka_producer = KafkaProducerService()
kafka_consumer = KafkaConsumerService()
