up:
	docker-compose -f docker-compose.yaml up -d

down:
	docker-compose -f docker-compose.yaml down && docker network prune --force

runapp:
	poetry run uvicorn myapplication.main:app --port 8000 --reload

db:
	docker exec -it postgres bash

testdb:
	docker exec -it postgres_test bash