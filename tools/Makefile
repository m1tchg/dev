## saves my favorite Pandoc options so I use the same commands in Vim and from the terminal

RM = rm
MAKEPRG = $(MAKE) --no-print-directory
MAKEDBG = $(MAKE)
PANDOCEXE = @pandoc.exe
PANDOCDBG = pandoc.exe
export PANDOCARGS
TOC  = --standalone --table-of-contents
CHECKLINKOPTS = --lua-filter=check-link-frags.lua  --quiet
CHECKLINKNAMEOPTS = --lua-filter=check-link-frag-names.lua  --quiet
REFLINKOPTS = --reference-links --reference-location=document
PRINTEXTLINKS = --lua-filter=print-ext-links.lua
PANDOCBASEOPTS = --wrap=none --atx-header
PANDOC = $(PANDOCEXE) $(PANDOCBASEOPTS) $(PANDOCARGS)
RSTOPTS = $(BASEFMTOUTOPTS)
MARKDOWNOPTS = +raw_html-native_divs-implicit_figures$(BASEFMTOUTOPTS)+old_dashes-raw_tex
TOMARKDOWN = markdown$(MARKDOWNOPTS)$(BASEFMTOUTOPTS)
FROMMARKDOWN = markdown$(MARKDOWNOPTS)-smart
RST = rst$(RSTOPTS)
HTMLOPTS = +raw_html-raw_tex-native_divs
HTML = html$(HTMLOPTS)$(BASEFMTOUTOPTS)
HTML4 = html4$(HTMLOPTS)
NOTABLEOPTS = -simple_tables-multiline_tables-grid_tables-pipe_tables
TIDYPANDOCBASEOPTS = -bare -quiet -utf8 --clean no --logical-emphasis yes --show-warnings 0 --tidy-mark no --quote-ampersand no --word-2000 yes -wrap 0 --drop-empty-paras no --drop-empty-elements no --indent no --vertical-space no --preserve-entities yes
TIDYXHTMLOPTS = --output-xhtml yes --doctype loose
TIDYPRG = @tidy.exe
TIDY = $(TIDYPRG) $(TIDYPANDOCBASEOPTS)

export TMP = _md
export TO = md
export FROM = html
export PANDOCARGS

export TOSRC = $(wildcard *.$(TO))
export FROMSRC := $(wildcard *.$(FROM))
GEN_FILES=\
					$(FROMSRC:.$(FROM)=.$(TMP))

## All markdown files in the working directory

export SRC = $(wildcard *.$(TMP))
HTMLSRC = $(wildcard *.html)
MDSRC = $(wildcard *.md)

TOHTML=$(SRC:.$(TMP)=.html)
FROMMD=$(MDSRC:.$(MEXT)=._md)

%.html: %.md
	cat $< |\
		$(MAKEPRG) _tohtml |\
		$(MAKEPRG) _xhtml > $@
		-htmlproofer.bat --check-external-hash $@

%.md: %.html
	cat $< |\
		$(MAKEPRG) _fromhtml > $@

%.txt: %.md
	cat $< |\
		$(MAKEPRG) _toplain > $@

%.rst: %.md
	cat $< |\
		$(MAKEPRG) _torst > $@

%._md: %.md
	cat $< |\
		$(MAKEPRG) _tomd > $@

pandoc:
	$(PANDOC) $(PANDOCARGS)

_fromhtml:
	$(PANDOC) -f $(HTML) -t $(TOMARKDOWN)$(NOTABLEOPTS) -o -

_frommd:
	$(PANDOC) -f $(FROMMARKDOWN) -t "$(RST)" -o -

_tohtml:
	$(PANDOC) -f $(FROMMARKDOWN) -t $(HTML) -o - 

_toxhtml:
		$(PANDOC) -f $(FROMMARKDOWN) -t $(HTML4) -o - 

_torst:
	$(PANDOC) -f $(FROMMARKDOWN) -t "$(RST)" -o -

_tomd:
	$(PANDOC) $(PANDOCBASEOPTS) -t "$(TOMARKDOWN)" -o -

_toplain:
	$(PANDOC) $(PANDOCBASEOPTS) -t plain -f "$(TOMARKDOWN)" -o -

toplain: $(SRC:.md=._md)
	cat $^ |\
		$(MAKEPRG) _toplain > $(SRC)
	$(MAKEPRG) clean FROM=md

todocx:
	$(PANDOCDBG) $(PANDOCBASEOPTS) -t "docx$(DOCXOPTS)" -o "$(SRC:.md=.docx)"  "$(SRC)"

fromdocx:
	$(PANDOCDBG) $(PANDOCBASEOPTS) -t "$(TOMARKDOWN)" -o "$(SRC:.docx=.md)"  "$(SRC)"

reflinks: $(SRC:.md=._md)
	cat $^ |\
		$(MAKEPRG) _reflinks > $(SRC)

_reflinks:
	$(PANDOC) $(PANDOCBASEOPTS) $(REFLINKOPTS) -f $(FROMMARKDOWN) -t $(TOMARKDOWN) -o -

_toc:
	$(PANDOC) $(PANDOCBASEOPTS) $(TOC) $(REFLINKOPTS) -f $(FROMMARKDOWN) -t $(TOMARKDOWN) -o -

toc: $(SRC:.md=._md)
	cat $^ |\
		$(MAKEPRG) _toc > $(SRC)
	$(MAKEPRG) clean FROM=md

striphids: $(SRC:.md=.$(TMP))
	cat $(SRC) |\
		$(MAKEPRG) _striphids |\
		$(MAKEPRG) _reflinks > $(SRC)
		$(MAKEPRG) clean FROMSRC=$(SRC) FROM=md

_striphids:
	$(PANDOC) $(PANDOCBASEOPTS) -f $(FROMMARKDOWN) -t $(TOMARKDOWN)-header_attributes -o -

__pandoc_xhtml:
	$(PANDOC) -s -f html$(HTMLOPTS) -t html4-smart -o -

_xhtml:
	-$(TIDY) $(TIDYXHTMLOPTS) || exit 0

_html:
	echo "$(TIDY)"
	-$(TIDY) || exit 0

clean:
	-$(RM) $(GEN_FILES)

fromhtml: $(HTMLSRC:.html=.$(TO))

md: $(FROMSRC:.$(FROM)=.md)

# pandoc: $(FROMSRC:.$(FROM)=$(TO))

##	$(MAKEPRG) clean FROM=html

wordcount:
	$(PANDOC) --lua-filter wordcount.lua $(git diff-tree --no-commit-id --name-only --relative -r $(REVFROM)..$(REVTO))

checkrstlinks: $(HTMLSRC:.html=.rst)
	cat > conf.py <<EOF \
		# Configuration file for the Sphinx documentation builder. \
		# \
		# This file only contains a selection of the most common options. For a full \
		# list see the documentation: \
		# https://www.sphinx-doc.org/en/master/usage/configuration.html \
		\
		# -- Path setup -------------------------------------------------------------- \
		\
		# If extensions (or modules to document with autodoc) are in another directory, \
		# add these directories to sys.path here. If the directory is relative to the \
		# documentation root, use os.path.abspath to make it absolute, like shown here. \
		# \
		# import os \
		# import sys \
		# sys.path.insert(0, os.path.abspath('.')) \
		\
		\
		# -- Project information ----------------------------------------------------- \
		\
		project = 'Asteria' \
		copyright = '2020, Asteria' \
		author = 'Asteria' \
		\
		\
		# -- General configuration --------------------------------------------------- \
		\
		# Add any Sphinx extension module names here, as strings. They can be \
		# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom \
		# ones. \
		extensions = [ \
		] \
		\
		# Add any paths that contain templates here, relative to this directory. \
		templates_path = ['_templates'] \
		\
		# List of patterns, relative to source directory, that match files and \
		# directories to ignore when looking for source files. \
		# This pattern also affects html_static_path and html_extra_path. \
		exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store'] \
		\
		\
		# -- Options for HTML output ------------------------------------------------- \
		\
		# The theme to use for HTML and HTML Help pages.  See the documentation for \
		# a list of builtin themes. \
		# \
		html_theme = 'alabaster' \
		\
		# Add any paths that contain custom static files (such as style sheets) here, \
		# relative to this directory. They are copied after the builtin static files, \
		# so a file named "default.css" will overwrite the builtin "default.css". \
		html_static_path = ['_static'] EOF
	sphinx-build -b linkcheck . /dev/null $<

#	$(PANDOC) $(CHECKLINKFRAGS) -f html $(wildcard *.html) 1>/dev/null

checklinks:
	$(PANDOC) $(CHECKLINKNAMEOPTS) $(SRC) 1>/dev/null
	htmlproofer.bat --check-external-hash $(SRC)

_xcheckstriplinks: $(TOSRC:.html=._md)
	cat $^ |\
		$(MAKEPRG) _striphids > _fromsrc._md
	#	$(PANDOC) $(PANDOCBASEOPTS) $(CHECKLINKOPTS) _fromsrc.md -o - 1>/dev/null


_linkreport:
	bash -c "$(PANDOCDBG) $(PANDOCBASEOPTS) $(CHECKLINKOPTS) $(CHECKLINKNAMEGREPOPTS) $(SRC) -o - 1>/dev/null"

Makefile:
	cp C:\users\mitch\dotfiles\dev\tools\Makefile .


