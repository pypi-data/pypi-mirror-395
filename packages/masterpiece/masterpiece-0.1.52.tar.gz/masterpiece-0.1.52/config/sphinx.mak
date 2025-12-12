# Makefile for Sphinx documentation
# Note: Sphinx has an issue with how it interprets relative image paths. 
# It re-interprets all relative paths to be relative to the location of its conf.py,
# which causes all relative paths to break unless explicitly adjusted for Sphinx.
# To work around this, this Makefile copies the necessary files from ../_static (where they 
# can be accessed by README.rst and other documents) into the docs/source/ directory,
# where Sphinx expects them in order to generate the HTML files. Quite a mess!

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?= -W
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = ../public

# Files to link from root to docs/source
FILES_TO_LINK = README.rst CONTRIBUTING.rst LICENSE.rst CHANGELOG.rst TODO.rst
STATIC_DIR =_static

# Link creation target (for specific files)
link-files:
	@for file in $(FILES_TO_LINK); do \
		cp "../$$file" "$(SOURCEDIR)/$$file"; \
	done

ensure-doctrees:
	@mkdir -p "$(BUILDDIR)/.doctrees"

# Copy ../_static  to source/_static
copy-static:
	cp -r ../$(STATIC_DIR) "$(SOURCEDIR)/";

# Copy _static and other files into source before generating HTML
html: ensure-doctrees link-files copy-static
	@echo "$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS) $(O)"
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown tar
