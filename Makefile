build:
	poetry build
	export WHEEL_PATH=`ls dist/file*.whl`
	envsubst '$$WHEEL_PATH' < pyoxidizer.template.bzl > pyoxidizer.bzl
	pyoxidizer build --release install
	cd ./build/x86*/release/install; \
	export VERSION=`poetry version -s`; \
	tar -zcf ../../../file_organizer-$$VERSION.tar.gz lib/ file_organizer
	rm -rf build/x86* dist pyoxidizer.bzl
