all: distclean dist upload

upload: dist
	twine upload dist/*

dist: distclean
	python setup.py sdist
	python setup.py bdist_wheel --universal

distclean:
	rm -rf dist/*
