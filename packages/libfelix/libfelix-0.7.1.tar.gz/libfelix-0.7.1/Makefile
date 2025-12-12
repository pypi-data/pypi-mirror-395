MAKEFLAGS += --always-make

default: ruff test

ruff:
	ruff format .
	ruff check .

mypy:
	mypy .

test:
	pytest --doctest-modules

build:
	python -m build --no-isolation

clean:
	rm -rf build/ dist/

pre-release: clean ruff test

push-with-tags:
	git push
	git push --tags

# release-test-pypi: pre-release
# 	twine upload --repository testpypi dist/*
#
upload:
	twine upload --repository pypi dist/*

minor-release: pre-release
	bump2version minor
	make build push-with-tags upload

patch-release: pre-release
	bump2version patch
	make build push-with-tags upload
