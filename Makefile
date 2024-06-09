build:
	poetry build
	export WHEEL_PATH=`ls dist/file*.whl`; \
	envsubst '$$WHEEL_PATH' < pyoxidizer.template.bzl > pyoxidizer.bzl
	poetry run pyoxidizer build --release install
	cd ./build/x86*/release/install; \
	tar -zcf ../../../file_organizer.tar.gz lib/ file_organizer
	rm -rf build/x86*

clear:
	rm -rf build dist pyoxidizer.bzl **/__pycache__

test:
	poetry run pytest -vv -s .

html:
	poetry run pytest --cov-report html

check:
	poetry run ruff --config pyproject.toml .
	poetry run bandit -c pyproject.toml -r .
	poetry run mypy --config-file pyproject.toml .
