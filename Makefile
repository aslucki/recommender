IMAGE_NAME=recommender
PORT ?= 8888
NAME ?= $(USER)_$(IMAGE_NAME)
DATA_PATH :=

.PHONY: build 

build:
	docker build -t $(IMAGE_NAME) .

dev:
	docker run --rm -ti  \
		--name $(NAME) \
		-p $(PORT):$(PORT) \
		-v $(PWD)/:/project \
		-v $(DATA_PATH):/data \
		-w "/project" \
		$(IMAGE_NAME)

lab:
	jupyter lab --ip=0.0.0.0 --port=$(PORT) --allow-root --no-browser