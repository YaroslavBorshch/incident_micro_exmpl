import asyncio

from src.services.kafka_service import kafka_consumer
from src.services.telegram_service import telegram_service


async def main():
    """чтение из топика инцидентов"""
    pass

if __name__ == '__main__':
    asyncio.run(main())
