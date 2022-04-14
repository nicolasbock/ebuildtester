all: distclean dist upload docs

upload: dist
	twine upload dist/*

dist: distclean
	python setup.py sdist
	python setup.py bdist_wheel --universal

docs:
	sphinx-apidoc --force --output-dir docs ebuildtester
	$(MAKE) -C docs

distclean:
	rm -rf dist/*

flatpak:
	flatpak-builder --force-clean build-dir io.github.nicolasbock.ebuildtester.yaml
