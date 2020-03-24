.PHONY: develop docs

PYTHON := python3

IN_VENV=. ./venv/bin/activate

venv/bin/activate:
	test -d venv || virtualenv venv --python=$(PYTHON)
	${IN_VENV} && pip install pip --upgrade

develop: venv/bin/activate
	${IN_VENV} && pip install -r requirements.txt && python setup.py develop

test: venv/bin/activate
	${IN_VENV} && pip install flake8 flake8-rst-docstrings flake8-docstrings flake8-import-order
	${IN_VENV} && flake8 aplanat \
		--import-order-style google --application-import-names aplanat \
		--statistics

.PHONY: clean
clean:
	rm -rf __pycache__ dist build venv aplanat.egg-info tmp

# Documentation
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = _build
PAPER         =
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
DOCSRC = docs
docs: venv
	${IN_VENV} && pip install sphinx sphinx_rtd_theme sphinx-argparse
	${IN_VENV} && cd $(DOCSRC) && $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(DOCSRC)/$(BUILDDIR)/html."
	touch $(DOCSRC)/$(BUILDDIR)/html/.nojekyll