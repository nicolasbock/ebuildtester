all: distclean dist upload docs

upload: dist
	twine upload dist/*

dist: distclean
	python -m build --sdist --wheel

docs:
	sphinx-apidoc --force --output-dir docs ebuildtester
	$(MAKE) -C docs

distclean:
	rm -rf dist/*

flatpak:
	flatpak-builder --force-clean build-dir io.github.nicolasbock.ebuildtester.yaml
