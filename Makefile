# Variables
IMAGE_NAME=quixpublic.azurecr.io/test-suite
CONTAINER_NAME=test-suite-container
DOCKER_FILE=Dockerfile
CONFIG_FILE=config.yaml
CA_FILE=ca.pem
PLATFORM ?= linux/amd64,linux/arm64
# Build the Docker image
build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) -f $(DOCKER_FILE) .

# Run the Docker container
run:
	@echo "Running Docker container with config.yaml..."
ifneq ("$(wildcard $(CA_FILE))","")
	@echo "Found ca.pem, mounting it as well."
	docker run --rm --name $(CONTAINER_NAME) \
		-v $(PWD)/$(CONFIG_FILE):/app/$(CONFIG_FILE) \
		-v $(PWD)/$(CA_FILE):/app/$(CA_FILE) \
		$(IMAGE_NAME)
else
	@echo "ca.pem not found, running without it."
	docker run --rm --name $(CONTAINER_NAME) \
		-v $(PWD)/$(CONFIG_FILE):/app/$(CONFIG_FILE) \
		$(IMAGE_NAME)
endif
#Publish to the public registry

publish:
	@echo "Publishing container to ..."
	docker buildx build --platform $(PLATFORM) --push  -f $(DOCKER_FILE) -t $(IMAGE_NAME) .


# Clean up Docker images and containers
clean:
	@echo "Cleaning up Docker images and containers..."
	docker rm -f $(CONTAINER_NAME) || true
	docker rmi -f $(IMAGE_NAME) || true

# Rebuild and run the container
rebuild: clean build run

.PHONY: build run clean rebuild
