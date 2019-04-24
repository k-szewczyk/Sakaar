### Variables ###

containers-tool = docker-compose
dev-dockerfile = -f docker-compose.yml -f docker-compose.dev.yml
staging-dockerfile = -f docker-compose.yml
backend-container = sakaar_backend


### Build & start app ###

.PHONY: build-dev
build-dev:
	$(containers-tool) $(dev-dockerfile) build

.PHONY: dev
dev:
	$(containers-tool) $(dev-dockerfile) up

.PHONY: backend-bash
backend-bash:
	docker exec -it $(backend-container) bash

