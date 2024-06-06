build:
	poetry version prerelease
	poetry build
	export WHEEL_PATH=`ls dist/file*.whl`; \
	envsubst '$$WHEEL_PATH' < pyoxidizer.template.bzl > pyoxidizer.bzl
	poetry run pyoxidizer build --release install
	cd ./build/x86*/release/install; \
	tar -zcf ../../../file_organizer.tar.gz lib/ file_organizer
	rm -rf build/x86*

clear:
	rm -rf build dist pyoxidizer.bzl **/__pycache__

major:
	git tag v$(shell poetry version -s major)
	git add pyproject.toml
	git commit --amend

minor:
	git tag v$(shell poetry version -s minor)
	git add pyproject.toml
	git commit --amend

patch:
	git tag v$(shell poetry version -s patch)
	git add pyproject.toml
	git commit --amend
