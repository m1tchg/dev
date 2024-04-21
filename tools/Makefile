# vim: set noexpandtab softtabstop=0:
#
# ## saves my favorite Pandoc options so I use the same commands in Vim and from the terminal

RM = rm
MAKEPRG = $(MAKE) --no-print-directory
MAKEDBG = $(MAKE)
PANDOCEXE = @pandoc $(ARGS)
PANDOCDBG = pandoc
HTMLPROOFEREXE = C:\tools\ruby30\bin\htmlproofer.bat
	export ARGS
	TOCDEPTH = 2
	TOC  = --standalone --table-of-contents --toc-depth=$(TOCDEPTH)
	CHECKLINKOPTS = --lua-filter=check-link-frags.lua --lua-filter=check-link-frag-names.lua --quiet
	CHECKLINKIDOPTS = --lua-filter=check-link-frags.lua  --quiet
	CHECKLINKNAMEOPTS = --lua-filter=check-link-frag-names.lua	--quiet
	REFLINKOPTS = --reference-links --reference-location=document
	PRINTEXTLINKS = --lua-filter=print-ext-links.lua
	PANDOCBASEOPTS = --markdown-headings=atx --wrap=preserve --tab-stop=2 --preserve-tabs=false
	PANDOC = $(PANDOCEXE) $(PANDOCBASEOPTS)
	TOMARKDOWN = markdown$(MARKDOWNOPTS)
	FROMMARKDOWN = markdown$(MARKDOWNOPTS)-smart-tex_math_dollars-tex_math_single_backslash-tex_math_double_backslash-markdown_in_html_blocks
	RST = rst$(RSTOPTS)
	BASEFMTOPTS = +raw_html-native_divs-implicit_figures+old_dashes-raw_tex-tex_math_dollars-tex_math_single_backslash-tex_math_double_backslash-markdown_in_html_blocks

TABLEOPTS = -simple_tables-multiline_tables+pipe_tables+grid_tables
GRIDTABLEOPTS = -simple_tables-multiline_tables-pipe_tables+grid_tables
NOTABLEOPTS = -simple_tables-multiline_tables-pipe_tables-grid_tables
MARKDOWNOPTS = +raw_html-native_divs-implicit_figures+old_dashes-raw_tex-tex_math_dollars$(NOTABLEOPTS)
HTMLOPTS = +raw_html-native_divs-tex_math_dollars-raw_tex-tex_math_dollars-tex_math_single_backslash-tex_math_double_backslash

HTML = html$(HTMLOPTS)
XHTML = html4$(HTMLOPTS)-smart
NOTABLEOPTS = -simple_tables-multiline_tables-grid_tables-pipe_tables
##TIDYCUSTOMTAGS = --custom-tags blocklevel --new-blocklevel-tags h:propertyname
TIDYBASEOPTS = -bare -quiet -utf8 --clean no --logical-emphasis yes --show-errors 2 --gnu-emacs --show-warnings 0 --tidy-mark no --quote-ampersand no --word-2000 yes -wrap 0 --drop-empty-paras no --drop-empty-elements no --indent no --vertical-space no --preserve-entities yes --literal-attributes true --lower-literals false --show-body-only auto
TIDYXMLOPTS = -xml --input-xml yes --indent auto --doctype loose --add-xml-space
TIDYXHTMLOPTS = --output-xhtml yes --doctype loose
TIDYHTMLOPTSOLD = -q -utf8 --show-errors 2 --tidy-mark no --quote-ampersand no --word-2000 yes -wrap 0 -xml
TIDYEXE = @tidy.exe
TIDY = $(TIDYEXE) $(TIDYBASEOPTS)
HTMLPROOFER = $(HTMLPROOFEREXE) --empty-alt-ignore --check-external-hash

export TMP = _md
export TO = md
export FROM = html
export INFMT = markdown
export PANDOCARGS

export TOSRC = $(wildcard *.$(TO))
export FROMSRC := $(wildcard *.$(FROM))
GEN_FILES=\
					$(FROMSRC:.$(FROM)=.$(TMP))

## All markdown files in the working directory

export SRC = $(wildcard *.$(FROM))
HTMLSRC = $(wildcard *.html)
MDSRC = $(wildcard *.md)

TOHTML=$(SRC:.$(TMP)=.html)
FROMMD=$(MDSRC:.$(MEXT)=._md)

.SILENT: _rehtml

%.html: %.md
	cat $< |\
		$(MAKEPRG) _tohtml |\
		$(MAKEPRG) _xhtml > $@
	$(HTMLPROOFER) $@

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
	cat $@ |\
		$(MAKEPRG) _checklinks

pandoc:
	$(PANDOC) $(PANDOCARGS)

_fromhtml:
	$(PANDOC) -f $(HTML) -t $(TOMARKDOWN) -o -

_frommd:
	$(PANDOC) -f $(FROMMARKDOWN) -t "$(RST)" -o -

_tohtml:
	$(PANDOC) -f $(FROMMARKDOWN) -t $(HTML) -o -

_toxhtml:
	$(PANDOC) -f $(FROMMARKDOWN) -t $(XHTML) -o -

_torst:
	$(PANDOC) -f $(FROMMARKDOWN) -t "$(RST)" -o -

_tomd:
	$(PANDOC) -f $(FROMMARKDOWN) -t "$(TOMARKDOWN)" -o -

_toplain:
	$(PANDOC) -t plain -f "$(TOMARKDOWN)" -o -

_tostandalone:
	$(PANDOC) -s -f $(FROMMARKDOWN) -t $(TO) -o -

_toc:
	$(PANDOC) $(TOC) $(REFLINKOPTS) -f $(FROMMARKDOWN) -t $(TOMARKDOWN) -o -

_tabletocsv:
	$(PANDOC) -F pantable2csv -f $(HTML) -t $(TOMARKDOWN) -o -

_csvtotable:
	$(PANDOC) -F pantable -f $(FROMMARKDOWN) -t $(HTML) -o -

_togridtable:
	$(PANDOC) -f $(HTML) -t $(TOMARKDOWN)$(GRIDTABLEOPTS) -o -

_fromgridtable:
	$(PANDOC) -f markdown$(MARKDOWNOPTS)$(GRIDTABLEOPTS) -t $(HTML) -o -

toplain: $(SRC:.md=._md)
	cat $^ |\
		$(MAKEPRG) _toplain > $(SRC)
	$(MAKEPRG) clean FROM=md

todocx:
	$(PANDOCDBG) $(PANDOCBASEOPTS) -t "docx$(DOCXOPTS)" -o "$(SRC:.md=.docx)"  "$(SRC)"

fromdocx:
	$(PANDOCDBG) $(PANDOCBASEOPTS) -t "$(TOMARKDOWN)" -o "$(SRC:.docx=.md)"  "$(SRC)"

toc: $(SRC:.md=._md)
	cat $^ |\
		$(MAKEPRG) _toc > $(SRC)
	$(MAKEPRG) clean FROM=md

striphids: $(SRC:.md=.$(TMP))
	cat $(SRC) |\
		$(MAKEPRG) _striphids |\
		$(MAKEPRG) _reflinks > $(SRC)
	$(MAKEPRG) clean FROMSRC=$(SRC) FROM=md

_stripcss:
	$(PANDOC) --lua-filter=strip-css.lua -f $(FROMMARKDOWN) -t $(HTML) -o -

_striphids:
	$(PANDOC) --lua-filter=regen-header-ids.lua -f $(FROMMARKDOWN) -t $(TOMARKDOWN) -o -

_xhtml:
	$(TIDY) $(TIDYXHTMLOPTS) ||:

_tidyxhtml:
	$(TIDY) $(TIDYXMLOPTS) $(TIDYXHTMLOPTS) ||:

_rehtml:
	$(MAKEPRG) _fromhtml PANDOCARGS=--wrap=none |\
		$(MAKEPRG) _tohtml PANDOCARGS=--wrap=preserve

_xml:
	@xmllint --recover -

_xmlformat:
	@xmllint --format pretty --recover -

_tidyxml:
	$(TIDY) $(TIDYXMLOPTS) ||:

_html:
	-$(TIDY) ||:

clean:
	-$(RM) $(FROMSRC:.$(FROM)=.$(TMP))

fromhtml: $(SRC:.html=.$(TO))

md: $(SRC:.$(FROM)=.md)

# pandoc: $(FROMSRC:.$(FROM)=$(TO))

##	$(MAKEPRG) clean FROM=html

wordcount:
	$(PANDOC) --lua-filter wordcount.lua $(git diff-tree --no-commit-id --name-only --relative -r $(REVFROM)..$(REVTO))

checkrstlinks: $(SRC:.html=.rst)
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
		# The theme to use for HTML and HTML Help pages.	See the documentation for \
		# a list of builtin themes. \
		# \
		html_theme = 'alabaster' \
		\
		# Add any paths that contain custom static files (such as style sheets) here, \
		# relative to this directory. They are copied after the builtin static files, \
		# so a file named "default.css" will overwrite the builtin "default.css". \
		html_static_path = ['_static'] EOF
	sphinx-build -b linkcheck . /dev/null $<

# $(PANDOC) $(CHECKLINKFRAGS) -f html $(wildcard *.html) 1>/dev/null
_tmp:
	mkdir /tmp

htmlproofer:
	-$(HTMLPROOFER)

_htmlproofer:
	@cat > out.html
	@$(HTMLPROOFER) out.html ||:
	@rm out.html

checklinks:
	$(MAKEPRG) $(SRC:.$(FROM)=.$(TO))
	echo $(SRC)
	cat $(SRC:.$(FROM)=.$(TO)) |\
		$(MAKEPRG) _striphids \|
	$(MAKEPRG) _checklinks

# Use PANDOCARGS to specify format -- default is markdown"

_checklinks:
	$(PANDOC) $(PANDOCBASEOPTS) --lua-filter=check-link-frags-nogrep.lua --lua-filter=check-link-frag-names-nogrep.lua --quiet -o - 1>/dev/null

_xcheckstriplinks: $(FROMSRC:.html=._md)

checklinknames:
	$(PANDOC) $(CHECKLINKNAMEOPTS) $(SRC) 1>/dev/null


_xcheckstriplinks: $(TOSRC:.html=._md)
	cat $^ |\
		$(MAKEPRG) _striphids > _fromsrc._md
	# $(PANDOC) $(CHECKLINKOPTS) _fromsrc.md -o - 1>/dev/null


_linkreport:
	bash -c "$(PANDOCDBG) $(PANDOCBASEOPTS) $(CHECKLINKOPTS) $(CHECKLINKNAMEGREPOPTS) $(SRC) -o - 1>/dev/null"

Makefile:
	cp C:\users\mitch\dotfiles\dev\tools\Makefile .


_rg:
	rg --smart-case --with-filename --hidden --no-heading -S --vimgrep --no-ignore-vcs --ignore-file $(HOME)/dotfiles/.rgignore -e '$(QUERY)'
