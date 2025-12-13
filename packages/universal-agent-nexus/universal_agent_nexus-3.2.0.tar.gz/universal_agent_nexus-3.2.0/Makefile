.PHONY: install lint test format clean

install:
	python -m venv .venv
	./.venv/Scripts/pip install --upgrade pip
	./.venv/Scripts/pip install -e .

lint:
	pytest -q tests || true

test:
	pytest -q tests

format:
	python -m black .

clean:
	rm -rf .venv __pycache__ .pytest_cache
