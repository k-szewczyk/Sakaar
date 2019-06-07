### Variables ###

containers-tool = docker-compose
dev-dockerfile = -f docker-compose.yml -f docker-compose.dev.yml
staging-dockerfile = -f docker-compose.yml
backend-container = sakaar_backend
FIXTURES-FILES= fixtures/battle_fixtures.json fixtures/halloffame_fixtures.json

### Build & start app ###

.PHONY: build-dev
build-dev:
	$(containers-tool) $(dev-dockerfile) build

.PHONY: dev
dev:
	$(containers-tool) $(dev-dockerfile) up

.PHONY: backend-django-shell
backend-django-shell:
	docker exec -it $(backend-container) python manage.py shell

.PHONY: backend-bash
backend-bash:
	docker exec -it $(backend-container) bash

.PHONY: migrations
migrations:
	docker exec $(backend-container) bash -c "./manage.py makemigrations; ./manage.py migrate"

.PHONY: django-shell
django-shell:
	docker exec $(backend-container) bash -c  "./manage.py shell"

.PHONY: load-fixtures
load-fixtures:
	docker exec -d $(backend-container) bash -c "./manage.py migrate && ./manage.py loaddata $(FIXTURES-FILES)"
