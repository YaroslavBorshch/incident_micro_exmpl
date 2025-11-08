.PHONY: help run up down restart logs build clean ps format lint

help:
	@echo "Доступные команды:"
	@echo "  make run      - Запустить все контейнеры и показать ссылку на Swagger"
	@echo "  make up       - Запустить все контейнеры"
	@echo "  make down     - Остановить все контейнеры"
	@echo "  make restart  - Перезапустить все контейнеры"
	@echo "  make logs     - Показать логи"
	@echo "  make build    - Пересобрать образы"
	@echo "  make clean    - Остановить и удалить все (включая данные БД)"
	@echo "  make ps       - Показать статус контейнеров"
	@echo "  make format   - Форматировать код (black + ruff --fix)"
	@echo "  make lint      - Проверить код (ruff)"

run:
	@echo "Запуск сервиса инцидентов..."
	@docker-compose up -d --build
	@echo ""
	@echo "Ожидание готовности сервисов..."
	@sleep 5
	@echo ""
	@echo "Сервис запущен!"
	@echo ""
	@echo "Swagger UI: http://localhost:3003/docs"
	@echo "ReDoc: http://localhost:3003/redoc"
	@echo "Health Check: http://localhost:3003/health"
	@echo ""
	@echo "Для просмотра логов используйте: make logs"

up:
	docker-compose up -d --build

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

build:
	docker-compose build --no-cache

clean:
	docker-compose down -v

ps:
	docker-compose ps

format:
	poetry run black src/
	poetry run ruff --fix src/

lint:
	poetry run ruff src/
