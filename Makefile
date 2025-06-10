black:
	poetry run python -m black -t py313 -l 120 --check .

black-fix:
	poetry run python -m black -t py313 -l 120 .

isort:
	poetry run python -m isort -l 120 -c .

isort-fix:
	poetry run python -m isort -l 120 .

lint:
	poetry run ruff check survey_studio_clients

lint-fix:
	poetry run ruff format survey_studio_clients

test:
	poetry run pytest ./survey_studio_clients -vv --cov=. --cov-report=term

all-prep:
	clear && make black-fix && make isort-fix && make lint && make test
