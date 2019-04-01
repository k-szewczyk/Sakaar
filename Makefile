### Variables ###
containers-tool = docker-compose
dev-dockerfile = -f docker-compose.yml -f docker-compose.dev.yml
staging-dockerfile = -f docker-compose.yml

### Build & start app ###
.PHONY: build-dev
build-dev:
	$(containers-tool) $(dev-dockerfile) build
