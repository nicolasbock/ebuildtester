all: distclean
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

distclean:
	rm -rf dist/*
