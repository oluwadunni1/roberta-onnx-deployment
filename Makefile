install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

format:
	black webapp/*.py

lint:
	# Disable 'Refactor' and 'Convention' checks to keep it practical
	pylint --disable=R,C webapp/app.py

test:
	# Run the unit tests
	pytest tests/

build:
	# Build the container
	docker build -t roberta-onnx:v1 .

run:
	# Run on port 5000
	docker run -p 5000:5000 roberta-onnx:v1

all: install lint test build