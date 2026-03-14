.PHONY: up down build restart test lint smoke logs clean health check-fake check-real

up:
	@echo "🚀 Starting TruthLens UA Analytics..."
	docker-compose up -d
	@echo "✅ API:       http://localhost:8000/docs"
	@echo "✅ Dashboard: http://localhost:8501"

down:
	docker-compose down

build:
	docker-compose up --build -d

restart:
	docker-compose restart api dashboard

test:
	docker-compose exec api pytest tests/ -v --tb=short

lint:
	docker-compose exec api ruff check app/ --select E,F,W

smoke:
	python scripts/smoke_test.py

logs:
	docker-compose logs -f --tail=50

migrate:
	docker-compose exec api alembic upgrade head

clean:
	docker-compose down -v --remove-orphans
	@echo "⚠️  All volumes removed"

health:
	@curl -s http://localhost:8000/health | python -m json.tool

check-fake:
	@curl -s -X POST http://localhost:8000/check \
	  -H "Content-Type: application/json" \
	  -d '{"text":"ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте до видалення!!!"}' \
	  | python -m json.tool

check-real:
	@curl -s -X POST http://localhost:8000/check \
	  -H "Content-Type: application/json" \
	  -d '{"text":"НБУ підвищив облікову ставку до 16% на засіданні Правління."}' \
	  | python -m json.tool
