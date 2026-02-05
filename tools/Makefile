# vim: set noexpandtab softtabstop=0:
#
# saves my favorite CLI options so I use the same commands in Vim and from the terminal

MAKEPRG = $(MAKE) -f $(HOME)/tools/Makefile --no-print-directory
MAKEDBG = $(MAKE) -f $(HOME)/tools/Makefile

HTMLTEST = htmltest
TOCDEPTH = 2
TOC  = --standalone --table-of-contents --toc-depth=$(TOCDEPTH)
CHECKLINKOPTS = --lua-filter=check-link-frags.lua --lua-filter=check-link-frag-names.lua --quiet
CHECKLINKIDOPTS = --lua-filter=check-link-frags.lua  --quiet
CHECKLINKNAMEOPTS = --lua-filter=check-link-frag-names.lua --quiet
REFLINKOPTS = --reference-links --reference-location=document
PRINTEXTLINKS = --lua-filter=print-ext-links.lua
PANDOCBASEOPTS = --markdown-headings=atx --wrap=preserve --tab-stop=2
PANDOC = @pandoc $(PANDOCBASEOPTS)
TOMARKDOWN = markdown$(MARKDOWNOPTS)
FROMMARKDOWN = markdown$(MARKDOWNOPTS)-raw_tex-smart-markdown_in_html_blocks-blank_before_header
BASEFMTOPTS = $(NOTEXMATHOPTS)+raw_html-native_divs-implicit_figures+old_dashes-markdown_in_html_blocks
NOTEXMATHOPTSOLD = -raw_tex-tex_math_dollars-tex_math_single_backslash-tex_math_double_backslash
MARKDOWNOPTS = +raw_html-native_divs-implicit_figures+old_dashes+wikilinks_title_after_pipe-smart
HTMLOPTS = +raw_html-native_divs-raw_tex
DOCXOPTS = --extract-media=.

HTML = html$(HTMLOPTS)
XHTML = html4$(HTMLOPTS)-smart
NOTABLEOPTS = -simple_tables-multiline_tables-grid_tables-pipe_tables
##TIDYCUSTOMTAGS = --custom-tags blocklevel --new-blocklevel-tags h:propertyname
TIDYBASEOPTS = -bare -quiet -utf8 --clean no --logical-emphasis yes --show-errors 2 --gnu-emacs --show-warnings 0 --tidy-mark no --quote-ampersand no --word-2000 yes -wrap 0 --drop-empty-paras no --drop-empty-elements no --indent no --vertical-space no --preserve-entities yes --literal-attributes true --lower-literals false --show-body-only auto
TIDYXMLOPTS = -xml --input-xml yes --indent auto --doctype loose --add-xml-space
TIDYXHTMLOPTS = --output-xhtml yes --doctype loose
TIDYHTMLOPTSOLD = -q -utf8 --show-errors 2 --tidy-mark no --quote-ampersand no --word-2000 yes -wrap 0 -xml
TIDY = @tidy $(TIDYBASEOPTS)

export PANDOCOPTS
export TO = md
export FROM = md
export TMP = _md

## All files in the working directory
export SRC = $(wildcard *.$(FROM))
GEN_FILES=\
					$(SRC:.$(FROM)=.$(TO))

.SILENT: _rehtml

%.md:
	$(PANDOC) -t $(TOMARKDOWN) -o $@ $(addsuffix .$(FROM),$(basename $@))

%.html: %.md
	cat $< |\
		$(MAKEPRG) _tohtml |\
		$(MAKEPRG) _xhtml > $@
	$(HTMLTEST) $@

%.docx: %.md
	cat $< |\
		$(MAKEPRG) _todocx > $@

%.txt: %.md
	cat $< |\
		$(MAKEPRG) _toplain > $@

_fromhtml:
	$(PANDOC) -f $(HTML) -t $(TOMARKDOWN) -o -

_fromodt:
	$(PANDOC) -f odt -t $(TOMARKDOWN) -o -

_fromdocx:
	$(PANDOC) -f docx -t $(TOMARKDOWN) -o -

_frompandoc:
	$(PANDOC) -s -f $(FROMMARKDOWN)-mark -t commonmark+yaml_metadata_block+strikeout -o -

_tohtml:
	$(PANDOC) -f $(FROMMARKDOWN)$(GRIDTABLEOPTS) -t $(HTML) -o -

_toxhtml:
	$(PANDOC) -f $(FROMMARKDOWN) -t $(XHTML) -o -

_todocx:
	$(PANDOC) -f $(FROMMARKDOWN) -t docx -o -

_toodt:
	$(PANDOC) -f $(FROMMARKDOWN) -t odt -o -

_topandoc:
	$(PANDOC) -s -f $(FROMMARKDOWN) -t $(TOMARKDOWN) -o -

_toplain:
	$(PANDOC) -t plain -f "$(TOMARKDOWN)" -o -

_tostandalone:
	$(PANDOC) -s -f $(FROMMARKDOWN) -t $(TO) -o -

_toobslink:
	$(PANDOC) -d toobsidian -f $(FROMMARKDOWN) -t commonmark+yaml_metadata_block -o -

_fromobslink:
	$(PANDOC) -d fromobsidian -f $(FROMMARKDOWN) -t commonmark+yaml_metadata_block -o -

_toc:
	$(PANDOC) $(TOC) -f $(FROMMARKDOWN) -t $(TOMARKDOWN) -o -

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

toc: $(SRC:.md=._md)
	cat $^ |\
		$(MAKEPRG) _toc > $(SRC)
	$(MAKEPRG) clean FROM=md

striphids: $(SRC:.md=.$(TMP))
	cat $(SRC) |\
		$(MAKEPRG) _striphids |\
		$(MAKEPRG) _reflinks > $(SRC)
	$(MAKEPRG) clean FROM=md

reflinks: $(SRC:.md=._md)
	cat $^ |\
		$(MAKEPRG) _reflinks > $(SRC)

_reflinks:
	$(PANDOC) $(REFLINKOPTS) -f $(FROMMARKDOWN) -t $(TOMARKDOWN) -o -

_stripcss:
	$(PANDOC) --lua-filter=strip-css.lua -f $(FROMMARKDOWN) -t $(HTML) -o -

_striphids:
	$(PANDOC) -f $(FROMMARKDOWN) -t $(TOMARKDOWN)-header_attributes -o -

_xhtml:
	$(TIDY) $(TIDYXHTMLOPTS) ||:

_tidyxhtml:
	$(TIDY) $(TIDYXMLOPTS) $(TIDYXHTMLOPTS) ||:

_rehtml:
	$(MAKEPRG) _fromhtml PANDOCOPTS=--wrap=none |\
		$(MAKEPRG) _tohtml PANDOCOPTS=--wrap=preserve

_repandoc:
	$(MAKEPRG) _tohtml PANDOCOPTS=--wrap=preserve |\
		$(MAKEPRG) _fromhtml PANDOCOPTS=--wrap=none

_xml:
	@xmllint --recover -

_xmlformat:
	@xmllint --format pretty --recover -

_tidyxml:
	$(TIDY) $(TIDYXMLOPTS) ||:

_html:
	-$(TIDY) ||:

clean:
	-rm $(SRC:.$(FROM)=.$(TMP))


wordcount:
	$(PANDOC) --lua-filter wordcount.lua $(git diff-tree --no-commit-id --name-only --relative -r $(REVFROM)..$(REVTO))

_htmltest:
	@cat > out.html
	@$(HTMLTEST) out.html ||:
	@rm out.html

checklinks:
	$(MAKEPRG) $(SRC:.$(FROM)=.$(TO))
	markdown-link-check -p -q $(SRC:.$(FROM)=.$(TO))

_checklinks:
	@cat > out.md
	@markdown-link-check -q out.md ||:
	@rm out.md

_checklinkfrags:
	$(PANDOC) --lua-filter=check-link-frags.lua --quiet -o -

checklinknames:
	$(PANDOC) $(CHECKLINKNAMEOPTS) $(SRC) 1>/dev/null

_linkreport:
	bash -c "$(PANDOCDBG) $(PANDOCBASEOPTS) $(CHECKLINKOPTS) $(CHECKLINKNAMEGREPOPTS) $(SRC) -o - 1>/dev/null"

_rg:
	rg --smart-case --with-filename --hidden --no-heading -S --vimgrep --no-ignore-vcs --ignore-file $(HOME)/dotfiles/.rgignore -e '$(QUERY)'
