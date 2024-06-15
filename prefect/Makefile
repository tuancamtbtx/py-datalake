-include .env

.PHONY:  package

docker-build:
	docker build -t $(DOCKER_IMAGE) .
run-server:
	python3 setup.py sdist bdist_wheel
