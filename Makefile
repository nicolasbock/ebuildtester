all: distclean dist upload docs

upload: dist
	twine upload dist/*

dist: distclean
	python setup.py sdist
	python setup.py bdist_wheel --universal

docs:
	$(MAKE) -C docs

distclean:
	rm -rf dist/*
